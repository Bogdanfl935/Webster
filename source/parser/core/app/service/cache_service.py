from app.utilities import url_joiner
from app.constants import endpoint_constants, serialization_constants
from app.utilities.api_utilities import unpack_response
import requests


def make_memory_usage_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.MEMORY_USAGE)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)


def make_last_parsed_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.LAST_PARSED)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)


def make_memory_usage_post(authenticated_user: str, memory_usage: int):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.MEMORY_USAGE)
    response = requests.post(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.MEMORY_USAGE_KEY: memory_usage})
    return unpack_response(response)
    

def make_last_parsed_post(authenticated_user: str, tag: str, url: str, memory_usage: int):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.LAST_PARSED)
    response = requests.post(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.URL_KEY: url,
        serialization_constants.TAG_KEY: tag,
        serialization_constants.MEMORY_USAGE_KEY: memory_usage
    })
    return unpack_response(response)