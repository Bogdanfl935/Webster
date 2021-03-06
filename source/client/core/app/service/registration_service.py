from app.constants import endpoint_constants
from flask import request, abort
from app.service import email_notification_service
from app.utilities.api_response_parser import *
import requests


def make_registration_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.REGISTRATION, json=request.form)
    return_content = None

    match response.status_code:
        case 201:
            # Registration successful
            confirmation_token, token_type = extract_confirmation_token_response(response.json())
            return_content, _ = email_notification_service.make_email_confirmation_post(confirmation_token, token_type)
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