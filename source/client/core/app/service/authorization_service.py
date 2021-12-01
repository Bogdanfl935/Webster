from functools import wraps
from app.constants import endpoint_constants, browser_constants
from app.utilities.api_response_parser import *
from app.service import cookie_service
from flask import request, make_response, abort
import requests

def require_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.cookies.get(browser_constants.ACCESS_TOKEN_COOKIE)
        response_object, authenticated_user = unpack_access_token(access_token)
        return f(response_object, authenticated_user, *args, **kwargs)            
    return decorated_function

def make_authorization_post(access_token: str):
    headers = dict(Authorization=access_token)
    response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.AUTHORIZATION, headers=headers)
    return_content = None

    if response.status_code == 200:
        # Access token is valid
        subject = extract_subject_response(response.json())
        return_content = dict(subject=subject)

    return return_content, response.status_code

def make_refreshment_post():
    authenticated_user = None
    return_content = make_response()
    status = 401

    if request.cookies.get(browser_constants.REFRESH_TOKEN_COOKIE) is not None:
        request_body = dict(refreshToken=request.cookies.get(browser_constants.REFRESH_TOKEN_COOKIE))
        response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.REFRESHMENT, json=request_body)
        status = response.status_code
        if response.status_code == 200:
            # Access token is valid
            access_token, token_type, authenticated_user = extract_refreshment_response(response.json())
            cookie_service.set_access_token_cookie(return_content, access_token, token_type)
    return return_content, status, authenticated_user

def unpack_access_token(access_token: str):
    # Anticipate bad request to avoid additional HTTP requests if not needed
    response, status = make_authorization_post(access_token) if access_token is not None else (None, 401)
    authenticated_user = None
    response_object = make_response()

    match status:
        case 200:
            authenticated_user = extract_subject_response(response)
        case 401:
            response_object, new_token_request_status, authenticated_user = make_refreshment_post()
            if new_token_request_status != 200:
                abort(status)
        case _:
            abort(status)

    return response_object, authenticated_user
            
    
