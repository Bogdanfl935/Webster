from bs4 import BeautifulSoup
from flask import Response, request, abort
from http import HTTPStatus
from app.constants import serialization_constants
from app.service import cache_service, configuration_service, image_parsing_service, url_parsing_service, generic_parsing_service
from app.service.executor_service import executor
import requests, html, logging, traceback


def parse() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    html_content = request.json.get(serialization_constants.CONTENT_KEY)
    page_url = request.json.get(serialization_constants.URL_KEY)
    message, status = _init_parsing(authenticated_user, html_content, page_url)

    if status != HTTPStatus.OK:
        abort(status, message)

    return Response(status = HTTPStatus.OK)

def get_last_parsed_content() -> Response:
    authenticated_user = request.args.get(serialization_constants.USERNAME_KEY)
    # return get_last_parsed(username)
    
def _init_parsing(authenticated_user, html_content):
    current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
    memory_limit = configuration_service.make_configuration_get(authenticated_user)
    message, response_status = None, HTTPStatus.OK

    if current_memory_usage < memory_limit:
        executor.submit(lambda: _parse(authenticated_user, memory_limit, html_content))
    else:
        response_status, message = "Maximum memory capacity exceeded", HTTPStatus.FORBIDDEN

    return message, response_status

def _parse(authenticated_user, memory_limit, html_content, page_url):
    # current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
    # continue_parsing = cache_service.make_parser_continuation_reading_post(authenticated_user)
    # tags = configuration_service.make_parser_configuration_get(authenticated_user)
    tags = ["a"]
    
    soup = BeautifulSoup(html_content, "lxml")
    for tag in tags:
        fetched_content = soup.find_all(tag)
        match tag:
            case 'img':
                executor.submit(
                    lambda: image_parsing_service.process_images(authenticated_user, fetched_content, memory_limit, page_url))
            case 'a':
                executor.submit(
                    lambda: url_parsing_service.process_anchors(authenticated_user, fetched_content, memory_limit, page_url))
            case _:
                executor.submit(
                    lambda: generic_parsing_service.process_generic_tag(
                        authenticated_user, fetched_content, memory_limit, page_url, tag))

    # TODO Store parsed tags in Redis cache

    # while current_memory_usage < memory_limit and continue_parsing is True:
    #     page_url, page_response = urls.pop(), requests.get(page_url)
    #     storage_service.make_pending_url_delete(authenticated_user, page_url)

    #     if page_response.status_code == HTTPStatus.OK:
    #         cache_service.make_last_url_post(authenticated_user, page_url)
    #         queue_publisher_service.dispatch_message(authenticated_user, page_response.text)

    #     if len(urls) == 0:
    #         urls = storage_service.make_next_url_post(authenticated_user)

    #     current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
    
# logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
#                         format="%(asctime)-15s %(levelname)-8s %(message)s")
# try:
#     _parse("alabila@gmail.com", 100000, html.unescape(requests.get("https://www.info.uvt.ro/").text), "https://www.info.uvt.ro/")
# except:
#     logging.log(level=logging.DEBUG, msg=traceback.format_exc())
# print(urlunparse(url_parsing_service._prepend_anchor_url_content(urlparse("//www.info.uvt.ro"), "https://www.info.uvt.ro")))


