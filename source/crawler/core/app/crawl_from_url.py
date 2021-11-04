import time

import requests
import constants
import endpoint_constants

def do_crawling(url):
    page = requests.get(url)

    dictPage = dict({'url': page.url, 'header': page.headers, 'html': page.content})

    send_to_parser = requests.post(url=f'http://127.0.0.1:80{endpoint_constants.PARSER}', data=dictPage)

    req_next_links = requests.post(url=f'http://127.0.0.1:80{endpoint_constants.NEXT_LINK}', data=dict({'quantity': constants.CRAWLER_NEXT_LINK_LIMIT}))


    if req_next_links.status_code != 200:
        time.sleep(2)
        req_next_links = requests.post(url=f'http://127.0.0.1:80{endpoint_constants.NEXT_LINK}', data=dict({'quantity': constants.CRAWLER_NEXT_LINK_LIMIT}))
        if req_next_links.status_code != 200:
            next_links = {'error_code': req_next_links.status_code}
        else:
            next_links = req_next_links.json()
            print(next_links)

    return next_links
