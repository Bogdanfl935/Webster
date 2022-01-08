from app.service import queue_publisher_service, cache_service, storage_service
from app.service import executor_service, configuration_service
from flask import abort, make_response, request, Response
from app.constants import serialization_constants
from http import HTTPStatus
import requests, logging, traceback


def start_crawling() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    start_url = request.json.get(serialization_constants.START_URL_KEY)
    message, status = _init_crawling(authenticated_user, start_url)
    
    if status != HTTPStatus.OK:
        abort(status, message)
        
    return Response(status = HTTPStatus.OK)
        
def get_crawler_status() -> Response:
    authenticated_user = request.args.get(serialization_constants.USERNAME_KEY)
    status_response, _ = cache_service.make_status_get(authenticated_user)
    last_url_response, _ = cache_service.make_last_url_get(authenticated_user)
    memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)

    response_content = status_response | last_url_response | memory_usage_response

    return make_response(response_content, HTTPStatus.OK)


def stop_crawling() -> Response:
    authenticated_user = request.json.get(serialization_constants.USERNAME_KEY)
    message, status = cache_service.make_continuation_writing_post(authenticated_user, continuation=False)

    if status != HTTPStatus.OK:
        abort(status, message)

    return Response(status = HTTPStatus.OK)


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
            executor_service.submit_task(lambda: _crawl(authenticated_user, memory_limit, start_url))
        else:
            message, response_status = "Crawler is already active", HTTPStatus.CONFLICT
    else:
        message, response_status = "Maximum memory capacity exceeded", HTTPStatus.FORBIDDEN
        
    return message, response_status
    

def _crawl(authenticated_user: str, memory_limit: int, start_url: str):
    try:
        __crawl_wrapped(authenticated_user, memory_limit, [start_url])
    finally:
        cache_service.make_status_writing_post(authenticated_user, active=False)

def __crawl_wrapped(authenticated_user: str, memory_limit: int, urls: list):
    memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)
    crawling_continuation_response, _ = cache_service.make_continuation_reading_post(authenticated_user)
    crawler_configuration_response, _ = configuration_service.make_configuration_get(authenticated_user)
    current_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
    continue_crawling = crawling_continuation_response.get(serialization_constants.CONTINUATION_KEY)
    configuration_options = crawler_configuration_response.get(serialization_constants.OPTIONS_KEY)
    # TODO Take into account crawler configuration options
    visited_urls = list()

    while len(urls) > 0 and current_memory_usage < memory_limit and continue_crawling is True:
            page_url = urls.pop()
            __process_page(authenticated_user, page_url)
            visited_urls.append(page_url)
            # Sporadic deadlock issue check
            logging.log(level=logging.WARNING, msg="==================PASSED QUEUE===================")
            if len(urls) == 0:
                if len(visited_urls) > 0: # Mark visited urls as visited
                    storage_service.make_pending_url_put(authenticated_user, visited_urls, visited=True)
                    visited_urls = list()
                urls = storage_service.make_sequential_next_url_post(authenticated_user)

            memory_usage_response, _ = cache_service.make_memory_usage_get(authenticated_user)
            crawling_continuation_response, _ = cache_service.make_continuation_reading_post(authenticated_user)
            current_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
            continue_crawling = crawling_continuation_response.get(serialization_constants.CONTINUATION_KEY)

    for visited_bool, url_list in {True: visited_urls, False: urls}.items():
        if len(url_list) > 0: # Set visited urls as visited, set leftover urls as not visited
            storage_service.make_pending_url_put(authenticated_user, url_list, visited_bool)
    

def __process_page(authenticated_user: str, page_url: str):
    try:
        page_response = requests.get(page_url)
    except requests.exceptions.RequestException:
        logging.log(level=logging.DEBUG, msg=traceback.format_exc())
        page_response = None

    if page_response is not None and page_response.status_code == HTTPStatus.OK:
        cache_service.make_last_url_post(authenticated_user, page_url)
        queue_publisher_service.dispatch_message(authenticated_user, page_response.text, page_url)
