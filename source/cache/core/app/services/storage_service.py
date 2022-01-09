from app.utilities import url_joiner
from app.utilities.api_utilities import unpack_response
from app.constants import endpoint_constants, serialization_constants
import requests

def make_memory_usage_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.MEMORY_USAGE)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_memory_usage_put(authenticated_user: str, memory_usage: int):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.MEMORY_USAGE)
    response = requests.put(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.MEMORY_USAGE_KEY: memory_usage})
    return unpack_response(response)