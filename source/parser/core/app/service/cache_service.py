from app.utilities import url_joiner
from app.constants import endpoint_constants
from app.utilities.api_utilities import unpack_response
import requests

def make_memory_usage_post(memory_usage: int):
    target_url = url_joiner.urljoin(endpoint_constants.CACHE_MS_URL, endpoint_constants.MEMORY_USAGE)
    response = requests.post(target_url, json=dict(username=authenticated_user, memoryUsage=memory_usage))
    return unpack_response(response)
