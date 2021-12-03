from app.service import authorization_service, email_notification_service
from app.constants import template_constants, endpoint_constants, main_endpoint_handler_constants
from flask import request, abort, render_template, redirect, url_for
from app.utilities.api_response_parser import *
from flask.templating import render_template_string
import requests

def make_password_forgotten_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.PASSWORD_FORGOTTEN, json=request.form)
    return_content = None
    
    match response.status_code:
        case 200:
            # Password forgotten token generation successful
            confirmation_token, token_type = extract_confirmation_token_response(response.json())
            return_content, _ = email_notification_service.make_password_forgotten_confirmation_post(confirmation_token, token_type)
        case 400:
            # Bad form data transmitted
            errors = extract_errors_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=errors)
        case 401:
            # Unauthorized
            message = extract_message_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=message)
        case _:
            abort(response.status_code)
    
    return return_content, response.status_code