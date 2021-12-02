import json
import time
import re

import requests
import constants
import endpoint_constants

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

def get_next_link():
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
