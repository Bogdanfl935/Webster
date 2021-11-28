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

  a_href_list = []

  for link in soup.find_all("a"):
    a_href_list.append(link.get("href").encode('latin1').decode('unicode-escape').replace('"', ''))

  for link in a_href_list:
    if link[0] == '.':
      index = a_href_list.index(link)
      link2=str(url) + link[1:]
      a_href_list.remove(link)
      a_href_list.insert(index, link2)


  next_links = {'links': a_href_list}

  return next_links
