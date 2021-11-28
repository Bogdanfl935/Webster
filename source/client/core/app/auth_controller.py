import requests
import sys
from flask import Blueprint, render_template, jsonify, request, abort, render_template_string, redirect, flash, url_for
from app.constants import endpoint_constants, template_constants, static_constants
from app.utilities.api_response_parser import *

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        registration_endpoint=f"{auth_controller.name}.{handle_registration_post.__name__}",
        authentication_endpoint=f"{auth_controller.name}.{handle_authentication_post.__name__}"
    )

@auth_controller.route(endpoint_constants.REGISTRATION, methods=['POST'])
def handle_registration_post():
    response = requests.post(endpoint_constants.AUTH_MS_URL+endpoint_constants.REGISTRATION, json=request.form)
    return_content = None

    match response.status_code:
        case 201:
            confirmation_token = extract_confirmation_token_response(response.json())
            return_content = dict(
                url=url_for(f"{auth_controller.name}.{handle_success_get.__name__}"),
                redirect=True
                )
        case 409:
            message = extract_message_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=message)
        case 400:
            errors = extract_errors_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=errors)
        case _:
            abort(response.status_code)
    
    return return_content, response.status_code

@auth_controller.route(endpoint_constants.SUCCESS, methods=['GET'])
def handle_success_get() -> str:
    return render_template_string("Not implemented")

@auth_controller.route(endpoint_constants.AUTHENTICATION, methods=['POST'])
def handle_authentication_post() -> str:
    return render_template_string("Not implemented")