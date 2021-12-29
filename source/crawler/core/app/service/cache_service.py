from app.utilities.api_utilities import unpack_response
from app.constants import endpoint_constants
from app.utilities import url_joiner
import requests


def make_memory_usage_get(authenticated_user):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.MEMORY_USAGE)
    parameterized_url = url_joiner.construct_parameterized_url(target_url, parameters=dict(username=authenticated_user))
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_status_reading_post(authenticated_user):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.CONCURRENT_STATUS_READING)
    response = requests.post(target_url, json=dict(username=authenticated_user))
    return unpack_response(response)

def make_continuation_reading_post(authenticated_user):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.CONCURRENT_CONTINUATION_READING)
    response = requests.post(target_url, json=dict(username=authenticated_user))
    return unpack_response(response)

def make_continuation_writing_post(authenticated_user: str, continuation: bool):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.CONCURRENT_CONTINUATION_WRITING)
    response = requests.post(target_url, json=dict(username=authenticated_user, continuation=continuation))
    return unpack_response(response)

def make_last_url_post(authenticated_user, page_url):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.LAST_URL)
    response = requests.post(target_url, json=dict(username=authenticated_user, lastUrl=page_url))
    return unpack_response(response)

def make_last_url_get(authenticated_user):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.LAST_URL)
    parameterized_url = url_joiner.construct_parameterized_url(target_url, parameters=dict(username=authenticated_user))
    response = requests.get(parameterized_url)
    return unpack_response(response)