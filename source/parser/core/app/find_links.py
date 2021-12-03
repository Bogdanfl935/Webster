import json
import time
import re
import requests
import constants
import endpoint_constants
from lxml import html
from bs4 import BeautifulSoup

def get_config():
    req_parser_config = requests.post(url=f'{endpoint_constants.CONFIG_MS_URL}{endpoint_constants.PARSER_CONFIG}',
                                      data=json.dumps({}))

    config_json = req_parser_config.json()

    return config_json

def parse_a_img(el_list, soup, url):
    parsed_content = dict()
    for tag in ["a", "img"]:
        link_list=[]
        if tag in el_list:
            for link in soup.find_all(tag):
                if link.get("href"):
                    link_list.append(link.get("href").encode('latin1').decode('unicode-escape').replace('"', ''))
                elif link.get("src"):
                    link_list.append(link.get("src").encode('latin1').decode('unicode-escape').replace('"', ''))

            for link in link_list:
                if link[0] == '.' or link[0] == '/':
                    index = link_list.index(link)
                    link2 = str(url) + link[1:]
                    link_list.remove(link)
                    link_list.insert(index, link2)

            if tag == "a":
                parsed_content['a'] = link_list
                el_list = list(filter(lambda a: a != 'a', el_list))
            elif tag == "img":
                parsed_content['img'] = link_list
                el_list = list(filter(lambda a: a != 'img', el_list))

    return el_list, parsed_content

def parse_all(el_list, soup):
    tags = dict()
    parsed_content = dict()

    for el in el_list:
        tags[el] = []
        for data in soup.find_all(el):
            tags[el].append(data.text)

        parsed_content[el] = tags[el]

    return el_list, parsed_content

def parsing_service(text, url):
    soup = BeautifulSoup(text, "lxml")

    config_json = get_config()
    el_list = config_json["specific-tag"]

    parsed_content_all = dict()
    parsed_content_links = dict()

    el_list, parsed_content_links = parse_a_img(el_list, soup, url)

    el_list, parsed_content_all = parse_all(el_list, soup)

    parsed_content_all.update(parsed_content_links)

    return parsed_content_all
