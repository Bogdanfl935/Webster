from app.constants import auth_endpoint_handler_constants, template_constants
from app.service import registration_service, authentication_service
from flask import render_template_string, render_template
from app.constants import endpoint_constants
from app.utilities.api_response_parser import *
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        registration_endpoint=auth_endpoint_handler_constants.HANDLE_REGISTRATION_POST,
        authentication_endpoint=auth_endpoint_handler_constants.HANDLE_AUTHENTICATION_POST,
        password_forgotten_endpoint=auth_endpoint_handler_constants.HANDLE_PASSWORD_FORGOTTEN_GET,
        confirmation_resending_endpoint=auth_endpoint_handler_constants.HANDLE_CONFIRMATION_RESENDING_GET,
        confirmation_endpoint=auth_endpoint_handler_constants.HANDLE_CONFIRMATION_POST
    )

@auth.route(endpoint_constants.CONFIRMATION_RESENDING, methods=['GET'])
def handle_confirmation_resending_get() -> str:
    return render_template_string("Not implemented")

@auth.route(endpoint_constants.CONFIRMATION+"/<token>", methods=['GET'])
def handle_confirmation_get(token) -> str:
    return render_template(template_constants.MODAL_CONFIRM_PATH)

@auth.route(endpoint_constants.PASSWORD_FORGOTTEN, methods=['GET'])
def handle_password_forgotten_get() -> str:
    return render_template_string("Not implemented")

@auth.route(endpoint_constants.REGISTRATION, methods=['POST'])
def handle_registration_post():
    return registration_service.make_registration_post()
    

@auth.route(endpoint_constants.AUTHENTICATION, methods=['POST'])
def handle_authentication_post() -> str:
    return authentication_service.make_authentication_post()

@auth.route(endpoint_constants.CONFIRMATION, methods=['POST'])
def handle_confirmation_post() -> str:
    return render_template_string("Not implemented")