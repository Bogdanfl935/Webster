from app.utilities import url_joiner
from app.constants import endpoint_constants, serialization_constants
from app.utilities.api_utilities import unpack_response
import requests


def make_parser_config_get(authenticated_user: str):
    target_url = url_joiner.urljoin(
        endpoint_constants.CONFIG_MS_URL, endpoint_constants.PARSER_CONFIGURATION)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)
