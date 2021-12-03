from app.service import authorization_service
from app.constants import template_constants, endpoint_constants, main_endpoint_handler_constants
from flask import request, abort, render_template, redirect, url_for
from app.utilities.api_response_parser import *
from flask.templating import render_template_string
import requests

def validate_confirmation_token():
    token = request.args.get('token')
    type = request.args.get('type')
    response, status = authorization_service.make_authorization_post(f"{type}{token}")
    return_content = None

    if status == 200:
        return_content = render_template(template_constants.SECTION_HOME_PATH, 
            include_modals = (
                template_constants.MODAL_CONFIRM_PATH,
                template_constants.MODAL_LOGIN_PATH
            ),
            confirmation_email = extract_subject_response(response),
            confirmation_token = token,
            token_type = type
        )
    elif status == 401:
        return_content = render_template(template_constants.SECTION_HOME_PATH,
            include_modals = (
                template_constants.MODAL_BAD_TOKEN_PATH,
                template_constants.MODAL_LOGIN_PATH
            )
        )
    else:
        abort(status)

    return return_content, status

def make_confirmation_post():
    confirmation_token = f"{request.form['type']}{request.form['token']}"
    headers = dict(Authorization=confirmation_token)
    response = requests.post(endpoint_constants.AUTH_MS_URL + endpoint_constants.CONFIRMATION, headers=headers)

    return_content = None

    match response.status_code:
        case 200:
            return_content = redirect(url_for(main_endpoint_handler_constants.HANDLE_HOME_GET))
        case 400 | 401 | 403:
            return_content = render_template(template_constants.SECTION_HOME_PATH,
                include_modals = (
                    template_constants.MODAL_BAD_TOKEN_PATH,
                    template_constants.MODAL_LOGIN_PATH
                )
            )
        case _:
            abort(response.status_code)

    return return_content, response.status_code

def render_multichoice_page():
    status = 200
    return_content = render_template(template_constants.SECTION_HOME_PATH,
            include_modals = (
                template_constants.MODAL_MULTI_CHOICE_PATH,
                template_constants.MODAL_LOGIN_PATH
            )
    )

    return return_content, status
