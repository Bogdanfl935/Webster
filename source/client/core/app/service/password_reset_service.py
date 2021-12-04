from app.service import authorization_service, email_notification_service
from app.constants import template_constants, endpoint_constants
from flask import request, abort, render_template
from app.utilities.api_response_parser import *
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

def make_password_resetting_post():
    reset_token = f"{request.form['type']}{request.form['token']}"
    request_body = dict(
        password = request.form['password'], 
        confirmPassword = request.form['confirmPassword']
    )
    headers = dict(Authorization=reset_token)
    response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.PASSWORD_RESETTING, headers=headers, json=request_body)
    return_content = None
    match response.status_code:
        case 200:
            return_content = dict(renderModalTemplate = render_template(template_constants.MODAL_ACCOUNT_UPDATED_PATH))
        case 400:
            # Bad form data transmitted
            errors = extract_errors_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=errors)
        case 401:
            return_content = dict(renderModalTemplate = render_template(template_constants.MODAL_BAD_TOKEN_PATH))
        case _:
            abort(response.status_code)

    return return_content, response.status_code

def do_prerender_validation():
    return authorization_service.validate_token(template_constants.MODAL_PASSWORD_RESET_PATH)