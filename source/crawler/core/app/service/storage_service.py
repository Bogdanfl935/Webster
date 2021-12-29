from app.constants import endpoint_constants, serialization_constants, storage_constants
from app.utilities import url_joiner
from app.utilities.api_utilities import unpack_response
import requests


def make_memory_limit_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.MEMORY_LIMIT)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_next_url_post(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.NEXT_URL)
    response = requests.post(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.QUANTITY_KEY: storage_constants.CRAWLER_URL_QUANTITY})
    return unpack_response(response)

def make_pending_url_put(authenticated_user: str, urls: list, visited: bool):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.URL_STORAGE)
    response = requests.put(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.URLS_KEY: urls,
        serialization_constants.VISITED_KEY: visited})
    return unpack_response(response)
