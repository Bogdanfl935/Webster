from app.constants import endpoint_constants
from app.utilities.url_joiner import construct_parameterized_url
from app.utilities.api_utilities import unpack_response
import requests

def make_status_get(authenticated_user: str) -> dict:
    target_url = construct_parameterized_url(endpoint_constants.PARSER_MS_URL + endpoint_constants.PARSER_STATUS,\
        dict(username=authenticated_user))
    response = requests.get(target_url)
    return unpack_response(response)