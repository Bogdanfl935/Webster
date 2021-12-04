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
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = 0
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        return found
    except Exception as e:
        return found
    else:
        found = start_crawling(url, html)
        return found


async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        await f.write(f"{url}\t{res}\n")
    return res


async def do_crawling(url):
    urls = [url]
    file = "output.txt"

    json_config = get_config()

    max_total_size = int(json_config["storage-limit"][0])
    max_total_size = max_total_size * 10 ** 6

    async with ClientSession() as session:
        tasks = []
        while len(urls) > 0 and max_total_size > 0:
            for url in urls:
                tasks.append(
                    functools.partial(write_one, file=file, url=url, session=session)
                )
                urls.remove(url)
            if len(urls) < 1:
                next_links_from_db = get_next_link()
                urls = next_links_from_db["urls"]
            result = await asyncio.gather(*[func() for func in tasks])
            max_total_size = max_total_size - result[-1]

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
