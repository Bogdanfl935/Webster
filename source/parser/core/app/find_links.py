import json
import time
import re
import requests
import constants
import endpoint_constants
from lxml import html
from bs4 import BeautifulSoup


def parse_urls(text, url):
    # TODO add gen on config MS

    soup = BeautifulSoup(text, "lxml")

    req_parser_config = requests.post(url=f'{endpoint_constants.CONFIG_MS_URL}{endpoint_constants.PARSER_CONFIG}',
                                        data=json.dumps({}))

    parsed_content = dict()

    config_json = req_parser_config.json()
    el_list = config_json["specific-tag"]

    a_href_list = []

    for link in soup.find_all("a"):
        if link.get("href"):
            a_href_list.append(link.get("href").encode('latin1').decode('unicode-escape').replace('"', ''))

    for link in a_href_list:
        if link[0] == '.' or link[0] == '/':
            index = a_href_list.index(link)
            link2 = str(url) + link[1:]
            a_href_list.remove(link)
            a_href_list.insert(index, link2)

    parsed_content['a'] = a_href_list
    el_list = list(filter(lambda a: a != 'a', el_list))

    if "img" in el_list:
        img_list = []
        for img in soup.find_all("img"):
            img_list.append(img.get("src").encode('latin1').decode('unicode-escape').replace('"', ''))

        for img in img_list:
            if img[0] == '.':
                index = img_list.index(img)
                img2 = str(url) + img[1:]
                img_list.remove(img)
                img_list.insert(img, img2)

        parsed_content['img'] = img_list
        el_list = list(filter(lambda a: a != 'img', el_list))

    tags = dict()

    for el in el_list:
        tags[el] = []
        for data in soup.find_all(el):
            tags[el].append(data.text)

        parsed_content[el] = tags[el]

    return parsed_content
