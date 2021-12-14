from flask import request, abort
from app.constants import endpoint_constants
from app.utilities.url_joiner import construct_parameterized_url
import requests

def make_status_get(authenticated_user: str) -> dict:
    target_url = construct_parameterized_url(endpoint_constants.PARSER_MS_URL + endpoint_constants.PARSER_STATUS,\
        dict(username=authenticated_user))
    response = requests.get(target_url)
    return_content = None
    
    match response.status_code:
        case 200:
            return_content = response.json()
        case 400:
            print(response.json())
            abort(400)
        case _:
            abort(response.status_code)
    
    return return_content, response.status_code