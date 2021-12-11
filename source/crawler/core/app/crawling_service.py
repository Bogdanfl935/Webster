import functools
import json
import sys
import time
import re
import requests
import constants
import endpoint_constants
import asyncio
import urllib
import aiofiles
import aiohttp
from aiohttp import ClientSession
from typing import IO
from app.get_total_size import total_size
from app.config import app, redis_mem_capacity
import redis
from rq import Worker, Queue, Connection

last_crawled_links = list()
active = bool()

def get_config():
    req_crawling_config = requests.post(url=f'{endpoint_constants.CONFIG_MS_URL}{endpoint_constants.CRAWLER_CONFIG}',
                                        data=json.dumps({}))
    json_config = req_crawling_config.json()

    return json_config


def start_crawling(url, html):
    dictPage = dict()

    dictPage["url"] = url
    dictPage["html"] = html

    dictPage = json.dumps(dictPage)

    parser_url = endpoint_constants.PARSER_MS_URL + endpoint_constants.PARSER

    send_to_parser = requests.post(url=parser_url, data=dictPage, headers={'Content-type': 'application/json'})
    parser_resp_json = send_to_parser.json()

    resp_size = total_size(parser_resp_json)

    return resp_size


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()

    last_crawled_links.append(url)
    global active
    active = True

    html = await resp.text()
    return html


async def process_crawling(url: str, session: ClientSession, **kwargs) -> set:
    size = 0
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        return size
    except Exception as e:
        return size
    else:
        size = start_crawling(url, html)
        return size


async def crawled_size(url: str, **kwargs) -> None:
    res = await process_crawling(url=url, **kwargs)
    if not res:
        return 0

    return res


async def do_crawling(url):
    urls = [url]
    file = "output.txt"

    json_config = get_config()

    max_total_size = int(json_config["storage-limit"][0])
    max_total_size = max_total_size * 10 ** 6
    redis_mem_capacity.set("user1", 0, nx=True)
    max_total_size = max_total_size - int(redis_mem_capacity.get("user1").decode())
    global active

    async with ClientSession() as session:
        tasks = []
        while len(urls) > 0 and max_total_size > 0:
            active = True
            for url in urls:
                tasks.append(
                    functools.partial(crawled_size, url=url, session=session)
                )
                urls.remove(url)
            if len(urls) < 1:
                next_links_from_db = get_next_link()
                urls = next_links_from_db["urls"]
            result = await asyncio.gather(*[func() for func in tasks])
            redis_mem_capacity.incrby("user1", result[-1])
            max_total_size = max_total_size - result[-1]
            if len(urls) == 0 or max_total_size <= 0:
                active = False
                break

    active = False

    return ('', 200)

def get_next_link():
    json_config = get_config()

    if 'True' in json_config["same-page"]:
        return json.dumps({"urls": []})

    post_to_next_link = {'quantity': constants.CRAWLER_NEXT_LINK_LIMIT}

    req_next_links = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.NEXT_LINK}',
                                   data=json.dumps(post_to_next_link))
    if req_next_links.status_code == 200:
        next_links = req_next_links.json()
    elif req_next_links.status_code != 200:
        time.sleep(2)
        req_next_links = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.NEXT_LINK}',
                                       data=json.dumps(post_to_next_link))
        if req_next_links.status_code != 200:
            next_links = {'error_code': req_next_links.status_code}
        else:
            next_links = req_next_links.json()

    return next_links

def get_last_crawled(username):
    return_dict = dict()
    return_dict["active"] = active
    return_dict["memoryUsage"] = int(redis_mem_capacity.get("user1").decode())

    if len(last_crawled_links) > 0:
        return_dict["url"] = last_crawled_links[-1]
        parsed_domain = urllib.request.urlparse(last_crawled_links[-1]).netloc
        if parsed_domain.startswith('www.'):
            parsed_domain = parsed_domain[4:]
        return_dict["domain"] = parsed_domain
    else:
        return_dict["url"] = None
        return_dict["domain"] = None

    return return_dict