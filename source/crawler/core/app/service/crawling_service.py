from app.service import queue_publisher_service, cache_service, storage_service, configuration_service
from flask import abort, make_response, request, Response
from app.service.executor_service import executor
from app.constants import serialization_constants
from http import HTTPStatus
import requests


def start_crawling() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    start_url = request.json.get(serialization_constants.START_URL_KEY)
    status, message = _init_crawling(authenticated_user, start_url)
    
    if status != HTTPStatus.OK:
        abort(status, message)
        
    return Response(status = HTTPStatus.OK)
        
def get_last_crawled_url() -> Response:
    authenticated_user = request.args.get(serialization_constants.USERNAME_KEY)
    return make_response(cache_service.make_last_url_get(authenticated_user))


def stop_crawling() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    return make_response(cache_service.make_continuation_writing_post(authenticated_user, False))

def _init_crawling(authenticated_user, start_url):
    current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
    memory_limit = configuration_service.make_configuration_get(authenticated_user)
    response_status, message = HTTPStatus.OK, None
    
    if current_memory_usage < memory_limit:
        crawler_active = cache_service.make_status_reading_post(authenticated_user)
        if not crawler_active:
            # Status reading flips activity flag to True, no subsequent writes are required
            executor.submit(lambda: _crawl(authenticated_user, memory_limit, [start_url]))
        else:
            response_status, message = HTTPStatus.CONFLICT, "Crawler is already active"
    else:
        response_status, message = HTTPStatus.FORBIDDEN, "Maximum memory capacity exceeded"
        
    return response_status, message
    
def _crawl(authenticated_user, memory_limit, urls):
    current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
    continue_crawling = cache_service.make_continuation_reading_post(authenticated_user)

    while len(urls) > 0 and current_memory_usage < memory_limit and continue_crawling is True:
        page_url, page_response = urls.pop(), requests.get(page_url)
        storage_service.make_pending_url_delete(authenticated_user, page_url)
        
        if page_response.status_code == HTTPStatus.OK:
            cache_service.make_last_url_post(authenticated_user, page_url)
            queue_publisher_service.dispatch_message(authenticated_user, page_response.text)
        
        if len(urls) == 0:
            urls = storage_service.make_next_url_post(authenticated_user)
            
        current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
