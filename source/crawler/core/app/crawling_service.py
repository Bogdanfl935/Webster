import json
import sys
import time
import re
import requests
import constants
import endpoint_constants

def get_config():
    req_crawling_config = requests.post(url=f'{endpoint_constants.CONFIG_MS_URL}{endpoint_constants.CRAWLER_CONFIG}',
                                        data=json.dumps({}))
    json_config = req_crawling_config.json()

    return json_config

def start_crawling(url):
    page = requests.get(url)

    dictPage = dict()
    dictPage["url"] = page.url
    dictPage["html"] = page.content.decode('utf-8')

    dictPage = json.dumps(dictPage)

    parser_url = endpoint_constants.PARSER_MS_URL + endpoint_constants.PARSER

    send_to_parser = requests.post(url=parser_url, data=dictPage, headers={'Content-type': 'application/json'})
    parser_resp_json = send_to_parser.json()

    resp_size = sys.getsizeof(parser_resp_json)

    return resp_size

def do_crawling(url):
    json_config = get_config()

    max_total_size = int(json_config["storage-limit"][0])
    max_total_size = max_total_size * 10 ** 6

    crawled_size = start_crawling(url)
    while crawled_size < max_total_size:
        if crawled_size == -1:
            next_urls = get_next_link()
            for el in next_urls["urls"]:
                crawled_size = start_crawling(el)
        else:
            max_total_size = max_total_size - crawled_size
            next_urls = get_next_link()
            for el in next_urls["urls"]:
                crawled_size = start_crawling(el)

    return ('', 200)

def get_next_link():
    json_config = get_config()

    if 'True' in json_config["same-page"]:
        return json.dumps({"urls": []})
    
    post_to_next_link = {'quantity': constants.CRAWLER_NEXT_LINK_LIMIT}

    req_next_links = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.NEXT_LINK}', data=json.dumps(post_to_next_link))
    if req_next_links.status_code == 200:
        next_links = req_next_links.json()
    elif req_next_links.status_code != 200:
        time.sleep(2)
        req_next_links = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.NEXT_LINK}', data=json.dumps(post_to_next_link))
        if req_next_links.status_code != 200:
            next_links = {'error_code': req_next_links.status_code}
        else:
            next_links = req_next_links.json()

    return next_links
