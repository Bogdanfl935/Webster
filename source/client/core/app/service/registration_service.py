from app.constants import endpoint_constants, auth_endpoint_handler_constants
from flask import request, abort, url_for
import json
from app.utilities.url_joiner import urljoin
from app.utilities.api_response_parser import *
import requests


def make_registration_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.REGISTRATION, json=request.form)
    return_content = None

    match response.status_code:
        case 201:
            # Registration successful
            confirmation_token, token_type = extract_confirmation_token_response(response.json())
            return_content, _ = make_email_confirmation_post(confirmation_token, token_type)
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

def make_email_confirmation_post(confirmation_token, token_type):
    form_details = request.form
    endpoint_parameters = f"{endpoint_constants.CONFIRMATION}?token={confirmation_token}&type={token_type}%20"
    target_url = urljoin(request.url_root, endpoint_parameters)
    request_body = dict(targetUrl=target_url, recipient=form_details["username"])
    response = requests.post(endpoint_constants.NOTIFICATION_MS_URL+endpoint_constants.EMAIL_CONFIRMATION, json=request_body)
    return_content = None

    match response.status_code:
        case 200:
            # Email confirmation has been sent successfully
            return_content = dict(
                url=url_for(auth_endpoint_handler_constants.HANDLE_CONFIRMATION_RESENDING_GET),
                redirect=True
            )
        case _:
            # Email delivery failure
            return_content = dict(
                url=request.referrer,
                redirect=True
            )
            print("Error occured: " + str(response.json()))
            pass

    return return_content, response.status_code