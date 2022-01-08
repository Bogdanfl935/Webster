from bs4 import BeautifulSoup
from flask import Response, request, abort, make_response
from http import HTTPStatus
from app.constants import serialization_constants, parsing_constants
from app.service import cache_service, configuration_service, image_parsing_service, url_parsing_service
from app.service import executor_service, generic_parsing_service, storage_service

def get_last_parsed_content() -> Response:
    authenticated_user = request.args.get(serialization_constants.USERNAME_KEY)
    content, status = cache_service.make_last_parsed_get(authenticated_user)
    response = Response(status=status)

    if content is not None:
        response = make_response(content, status)

    return response
    
def init_parsing(authenticated_user, html_content, page_url):
    memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)
    memory_limit_response, _ = storage_service.make_memory_limit_get(authenticated_user)
    current_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
    memory_limit = memory_limit_response.get(serialization_constants.MEMORY_LIMIT_KEY)

    if current_memory_usage < memory_limit:
        executor_service.submit_task(lambda: _parse(authenticated_user, memory_limit, html_content, page_url))
    else:
        abort(HTTPStatus.FORBIDDEN, "Maximum memory capacity exceeded") 

def _parse(authenticated_user, memory_limit, html_content, page_url):
    parser_config_response, _ = configuration_service.make_parser_config_get(authenticated_user)
    tags = list(set(parser_config_response.get(serialization_constants.TAGS_KEY)))
    
    soup = BeautifulSoup(html_content, "lxml")
    for tag in tags:
        fetched_content = soup.find_all(tag)
        match tag:
            case parsing_constants.IMAGE_TAG:
                executor_service.submit_task(
                    lambda: image_parsing_service.process_images(
                        authenticated_user, fetched_content, memory_limit, page_url))
            case _:
                executor_service.submit_task(
                    lambda: generic_parsing_service.process_generic_tag(
                        authenticated_user, fetched_content, memory_limit, page_url, tag))
    # Parse mandatory anchor tags
    anchors = soup.find_all(parsing_constants.ANCHOR_TAG)
    executor_service.submit_task(
        lambda: url_parsing_service.process_anchors(authenticated_user, anchors, memory_limit, page_url))


