from app.constants import endpoint_constants, auth_endpoint_handler_constants
from flask import request, abort, url_for
from app.utilities.api_response_parser import *
import requests


def make_registration_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.REGISTRATION, json=request.form)
    return_content = None

    match response.status_code:
        case 201:
            # Registration successful
            confirmation_token = extract_confirmation_token_response(response.json())
            return_content = dict(
                url=url_for(auth_endpoint_handler_constants.HANDLE_CONFIRMATION_RESENDING_GET),
                redirect=True
                )
        case 400:
            # Bad form data transmitted
            errors = extract_errors_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=errors)
        case 409:
            # Conflict - Username already taken
            message = extract_message_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=message)
        case _:
            abort(response.status_code)
    
    return return_content, response.status_code