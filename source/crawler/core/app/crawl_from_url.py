import json
import time

import requests
import constants
import endpoint_constants

def do_crawling(url):
    page = requests.get(url)

    # dictPage = dict({'url': page.url, 'header': page.headers, 'html': page.content})

    # send_to_parser = requests.post(url=f'{endpoint_constants.PARSER_MS_URL}{endpoint_constants.PARSER}', data=dictPage)

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
