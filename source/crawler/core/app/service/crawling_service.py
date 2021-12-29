from app.service import queue_publisher_service, cache_service, storage_service, configuration_service
from flask import abort, make_response, request, Response
from app.service.executor_service import executor
from app.constants import serialization_constants
from http import HTTPStatus
import requests


def start_crawling() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    start_url = request.json.get(serialization_constants.START_URL_KEY)
    message, status = _init_crawling(authenticated_user, start_url)
    
    if status != HTTPStatus.OK:
        abort(status, message)
        
    return Response(status = HTTPStatus.OK)
        
def get_last_crawled_url() -> Response:
    authenticated_user = request.args.get(serialization_constants.USERNAME_KEY)
    return make_response(cache_service.make_last_url_get(authenticated_user))


def stop_crawling() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    return make_response(cache_service.make_continuation_writing_post(authenticated_user, False))


def _init_crawling(authenticated_user: str, start_url: str):
    memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)
    memory_limit_response, _ = storage_service.make_memory_limit_get(authenticated_user)
    current_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
    memory_limit = memory_limit_response.get(serialization_constants.MEMORY_LIMIT_KEY)
    message, response_status = None, HTTPStatus.OK 
    
    if current_memory_usage < memory_limit:
        crawler_status_response, _ = cache_service.make_status_reading_post(authenticated_user)
        crawler_active = crawler_status_response.get(serialization_constants.ACTIVE_KEY)
        if not crawler_active:
            # Status reading flips activity flag to True, no subsequent writes are required
            executor.submit(lambda: _crawl(authenticated_user, memory_limit, [start_url]))
        else:
            message, response_status = "Crawler is already active", HTTPStatus.CONFLICT
    else:
        message, response_status = "Maximum memory capacity exceeded", HTTPStatus.FORBIDDEN
        
    return message, response_status
    

def _crawl(authenticated_user: str, memory_limit: int, urls: list):
    memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)
    crawling_continuation_response, _ = cache_service.make_continuation_reading_post(authenticated_user)
    crawler_configuration_response, _ = configuration_service.make_configuration_get(authenticated_user)
    current_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
    continue_crawling = crawling_continuation_response.get(serialization_constants.CONTINUATION_KEY)
    configuration_options = crawler_configuration_response.get(serialization_constants.OPTIONS_KEY)
    # TODO Take into account crawler configuration options
    visited_urls = list()

    while len(urls) > 0 and current_memory_usage < memory_limit and continue_crawling is True:
        page_url, page_response = urls.pop(), requests.get(page_url)
        
        if page_response.status_code == HTTPStatus.OK:
            visited_urls.append(page_url)
            cache_service.make_last_url_post(authenticated_user, page_url)
            queue_publisher_service.dispatch_message(authenticated_user, page_response.text)
        
        if len(urls) == 0:
            next_urls_response, _ = storage_service.make_next_url_post(authenticated_user)
            urls = next_urls_response.get(serialization_constants.URLS_KEY)
            
        memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)
        current_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)

    for visited_bool, url_list in {True: visited_urls, False: urls}.items():
        if len(url_list) > 0: # Set visited urls as visited, set leftover urls as not visited
            storage_service.make_pending_url_put(authenticated_user, url_list, visited_bool)
