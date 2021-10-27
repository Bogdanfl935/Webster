import requests

def do_crawling(url):
    page = requests.get(url)

    dictPage = dict({'url': page.url, 'header': page.headers, 'html': page.content})

    res = requests.post('https://example.org//parser', data=dictPage)

    return True
