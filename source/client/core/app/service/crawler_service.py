from flask import request, abort
from app.constants import endpoint_constants
from app.utilities.url_joiner import construct_parameterized_url
import requests

def make_status_get(authenticated_user: str) -> dict:
    target_url = construct_parameterized_url(endpoint_constants.CRAWLER_MS_URL + endpoint_constants.CRAWLER_STATUS,\
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

def make_crawler_start_post(authenticated_user: str) -> dict:
    request_body = dict(username=authenticated_user) | request.form
    response = requests.post(endpoint_constants.CRAWLER_MS_URL + endpoint_constants.CRAWLER_START, json=request_body)
    return_content = None
    
    match response.status_code:
        case 200:
            return_content = response.json()
        case 400:
            print(response.json())
            abort(400)
        case _:
            pass
            #abort(response.status_code)
    
    return return_content, response.status_code

def make_crawler_stop_post(authenticated_user: str) -> dict:
    request_body = dict(username=authenticated_user)
    response = requests.post(endpoint_constants.CRAWLER_MS_URL + endpoint_constants.CRAWLER_STOP, json=request_body)
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