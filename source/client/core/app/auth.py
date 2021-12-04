from app.constants import auth_endpoint_handler_constants
from app.service import registration_service, authentication_service,\
authorization_service, confirmation_service, password_reset_service
from app.service.authorization_service import require_access_token
from app.constants import endpoint_constants
from app.utilities.api_response_parser import *
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        registration_endpoint=auth_endpoint_handler_constants.HANDLE_REGISTRATION_POST,
        authentication_endpoint=auth_endpoint_handler_constants.HANDLE_AUTHENTICATION_POST,
        password_resetting_endpoint=auth_endpoint_handler_constants.HANDLE_PASSWORD_RESETTING_POST,
        password_change_endpoint=auth_endpoint_handler_constants.HANDLE_PASSWORD_FORGOTTEN_POST,
        confirmation_resending_get_endpoint=auth_endpoint_handler_constants.HANDLE_CONFIRMATION_RESENDING_GET,
        confirmation_resending_post_endpoint=auth_endpoint_handler_constants.HANDLE_CONFIRMATION_RESENDING_POST,
        confirmation_endpoint=auth_endpoint_handler_constants.HANDLE_CONFIRMATION_POST
    )

# GET ENDPOINTS

@auth.route(endpoint_constants.CONFIRMATION_RESENDING, methods=['GET'])
def handle_confirmation_resending_get() -> tuple:
    return confirmation_service.render_multichoice_page()

@auth.route(endpoint_constants.CONFIRMATION, methods=['GET'])
def handle_confirmation_get() -> tuple:
    return confirmation_service.do_prerender_validation()

@auth.route(endpoint_constants.PASSWORD_RESETTING, methods=['GET'])
def handle_password_resetting_get() -> tuple:
    return password_reset_service.do_prerender_validation()

# POST ENDPOINTS

@auth.route(endpoint_constants.REGISTRATION, methods=['POST'])
def handle_registration_post() -> tuple:
    return registration_service.make_registration_post()
    
@auth.route(endpoint_constants.AUTHENTICATION, methods=['POST'])
def handle_authentication_post() -> tuple:
    return authentication_service.make_authentication_post()

@auth.route(endpoint_constants.REFRESHMENT, methods=['POST'])
def handle_refreshment_post() -> tuple:
    return authorization_service.make_refreshment_post()

@auth.route(endpoint_constants.CONFIRMATION, methods=['POST'])
def handle_confirmation_post() -> tuple:
    return confirmation_service.make_confirmation_post()

@auth.route(endpoint_constants.CONFIRMATION_RESENDING, methods=['POST'])
def handle_confirmation_resending_post() -> tuple:
    return confirmation_service.make_confirmation_resending_post()

@auth.route(endpoint_constants.PASSWORD_FORGOTTEN, methods=['POST'])
def handle_password_forgotten_post() -> tuple:
    return password_reset_service.make_password_forgotten_post()

@auth.route(endpoint_constants.PASSWORD_RESETTING, methods=['POST'])
def handle_password_resetting_post() -> tuple:
    return password_reset_service.make_password_resetting_post()

