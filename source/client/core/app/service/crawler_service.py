from flask import request
from app.constants import endpoint_constants, serialization_constants
from app.utilities.url_joiner import construct_parameterized_url
from app.utilities.api_utilities import unpack_response
import requests

def make_status_get(authenticated_user: str) -> dict:
    target_url = construct_parameterized_url(endpoint_constants.CRAWLER_MS_URL + endpoint_constants.CRAWLER_STATUS,
        {serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(target_url)
    return unpack_response(response)

def make_crawler_start_post(authenticated_user: str) -> dict:
    request_body = {serialization_constants.USERNAME_KEY: authenticated_user} | request.form
    response = requests.post(endpoint_constants.CRAWLER_MS_URL + endpoint_constants.CRAWLER_START, json=request_body)
    return unpack_response(response)

def make_crawler_stop_post(authenticated_user: str) -> dict:
    request_body = {serialization_constants.USERNAME_KEY: authenticated_user}
    response = requests.post(endpoint_constants.CRAWLER_MS_URL + endpoint_constants.CRAWLER_STOP, json=request_body)
    return unpack_response(response)