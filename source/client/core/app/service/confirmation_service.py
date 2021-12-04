from app.service import authorization_service, email_notification_service
from app.constants import template_constants, endpoint_constants
from app.constants.token_scope import TokenScope
from flask import request, abort, render_template
from app.utilities.api_response_parser import *
import requests

def do_prerender_validation() -> tuple:
    return authorization_service.validate_token(template_constants.MODAL_CONFIRM_PATH, TokenScope.CONFIRM)

def make_confirmation_post() -> tuple:
    confirmation_token = f"{request.form['type']}{request.form['token']}"
    headers = dict(Authorization=confirmation_token)
    response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.CONFIRMATION, headers=headers)

    return_content = None

    match response.status_code:
        case 200:
            return_content = dict(renderModalTemplate = render_template(template_constants.MODAL_ACCOUNT_UPDATED_PATH))
        case 400 | 401 | 403:
            return_content = dict(renderModalTemplate = render_template(template_constants.MODAL_BAD_TOKEN_PATH))
        case _:
            abort(response.status_code)

    return return_content, response.status_code

def make_confirmation_resending_post() -> tuple:
    response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.CONFIRMATION_RESENDING, json=request.form)
    return_content = None

    match response.status_code:
        case 200:
            confirmation_token, token_type = extract_confirmation_token_response(response.json())
            return_content, _ = email_notification_service.make_email_confirmation_post(confirmation_token, token_type)
        case 400:
            # Bad form data transmitted
            errors = extract_errors_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=errors)
        case 401 | 403:
            message = extract_message_response(response.json())
            # Return errors as JSON for client-side processing
            return_content = dict(error=message)
        case _:
            abort(response.status_code)

    return return_content, response.status_code

def render_multichoice_page() -> tuple:
    status = 200
    return_content = render_template(template_constants.SECTION_HOME_PATH,
            include_modals = (template_constants.MODAL_MULTI_CHOICE_PATH,)
    )

    return return_content, status
