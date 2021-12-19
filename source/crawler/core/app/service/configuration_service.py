from app.constants import endpoint_constants
from app.utilities import url_joiner, api_utilities
import requests

def make_configuration_get(authenticated_user):
    target_url = url_joiner.urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.CRAWLER_CONFIGURATION)
    parameterized_url = url_joiner.construct_parameterized_url(target_url, parameters=dict(username=authenticated_user))
    response = requests.get(parameterized_url)
    return api_utilities.unpack_response(response)
