import requests
from flask import Blueprint, render_template, jsonify, request, abort, render_template_string, redirect, flash, url_for
from app.constants import endpoint_constants, template_constants, static_constants
from app.utilities.api_response_parser import *

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        registration_endpoint=f"{auth_controller.name}.{handle_registration_post.__name__}",
        authentication_endpoint=f"{auth_controller.name}.{handle_authentication_post.__name__}",
        password_forgotten_endpoint=f"{auth_controller.name}.{handle_password_forgotten_get.__name__}"
    )

@auth_controller.route(endpoint_constants.CONFIRMATION_RESENDING, methods=['GET'])
def handle_confirmation_resending_get() -> str:
    return render_template_string("Not implemented")

@auth_controller.route(endpoint_constants.PASSWORD_FORGOTTEN, methods=['GET'])
def handle_password_forgotten_get() -> str:
    return render_template_string("Not implemented")

@auth_controller.route(endpoint_constants.REGISTRATION, methods=['POST'])
def handle_registration_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.REGISTRATION, json=request.form)
    return_content = None

    match response.status_code:
        case 201:
            # Registration successful
            confirmation_token = extract_confirmation_token_response(response.json())
            return_content = dict(
                url=url_for(f"{auth_controller.name}.{handle_confirmation_resending_get.__name__}"),
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

@auth_controller.route(endpoint_constants.AUTHENTICATION, methods=['POST'])
def handle_authentication_post() -> str:
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.AUTHENTICATION, json=request.form)
    return_content = None

    match response.status_code:
        case 200:
            # Authentication successful
            # access_token, refresh_token, token_type = extract_confirmation_token_response(response.json())
            return_content = dict(
                url=request.referrer,
                redirect=True
                )
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
                url=url_for(f"{auth_controller.name}.{handle_confirmation_resending_get.__name__}"),
                redirect=True
            )
        case _:
            abort(response.status_code)
    
    return return_content, response.status_code