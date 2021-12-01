from app.constants import endpoint_constants, auth_endpoint_handler_constants, browser_constants
from flask import request, abort, url_for, make_response
from app.utilities.api_response_parser import *
from app.service import cookie_service
import requests


def make_authentication_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.AUTHENTICATION, json=request.form)
    return_content = None

    match response.status_code:
        case 200:
            # Authentication successful
            access_token, refresh_token, token_type = extract_access_token_response(response.json())
            response_dict = dict(
                url=request.referrer,
                redirect=True
            )
            return_content = make_response(response_dict)
            cookie_service.set_access_token_cookie(return_content, access_token, token_type)
            cookie_service.set_refresh_token_cookie(return_content, refresh_token)
        case 400:
            # Bad form data transmitted
            errors = extract_errors_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=errors)
        case 401:
            # Authentication failed
            message = extract_message_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=message)
        case 403:
            # Authentication forbidden - Account not yet confirmed
            return_content = dict(
                url=url_for(auth_endpoint_handler_constants.HANDLE_CONFIRMATION_RESENDING_GET),
                redirect=True
            )
        case _:
            abort(response.status_code)

    return return_content, response.status_code
