from app.utilities import url_joiner
from app.utilities.api_utilities import unpack_response
from app.constants import endpoint_constants, serialization_constants
import requests

def make_memory_limit_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.MEMORY_LIMIT)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_content_source_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.CONTENT_SOURCE)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)