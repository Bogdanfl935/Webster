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

def do_crawling(url):
    page = requests.get(url)

    # url_escaped = re.escape(page.url.encode('latin1'))

    dictPage = dict()
    dictPage["url"] = page.url
    dictPage["html"] = page.content.decode('utf-8')

    dictPage = json.dumps(dictPage)

    # print(dictPage)

    # dictPage = json.dumps(dict({"url": page.url, "header": headers_escaped, "html": page.content}))

    parser_url = endpoint_constants.PARSER_MS_URL + endpoint_constants.PARSER

    send_to_parser = requests.post(url=parser_url, data=dictPage, headers={'Content-type': 'application/json'})
    parser_resp_json = send_to_parser.json()

    json_config = get_config()

    max_size = int(json_config["storage-limit"][0])
    max_size = max_size * 10**6

    if sys.getsizeof(parser_resp_json) > max_size:
        return False

    return True


def get_next_link():
    json_config = get_config()

    if 'True' in json_config["same-page"]:
        return json.dumps({"urls": []})
    
    post_to_next_link = {'quantity': constants.CRAWLER_NEXT_LINK_LIMIT}

    req_next_links = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.NEXT_LINK}', data=json.dumps(post_to_next_link))
    # print(req_next_links)
    if req_next_links.status_code == 200:
        next_links = req_next_links.json()
    elif req_next_links.status_code != 200:
        time.sleep(2)
        req_next_links = requests.post(url=f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.NEXT_LINK}', data=json.dumps(post_to_next_link))
        if req_next_links.status_code != 200:
            next_links = {'error_code': req_next_links.status_code}
        else:
            next_links = req_next_links.json()
            print(next_links)

    return next_links
