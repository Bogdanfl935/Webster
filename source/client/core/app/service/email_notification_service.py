from app.constants import endpoint_constants, template_constants
from flask import request
from app.utilities.url_joiner import urljoin
from app.utilities.api_response_parser import *
from flask.templating import render_template
import requests

def make_password_forgotten_confirmation_post(confirmation_token: str, token_type: str) -> tuple:
    request_body = construct_request_body(confirmation_token, token_type, endpoint_constants.PASSWORD_RESETTING)
    return send_notification_request(endpoint_constants.EMAIL_PASSWORD_RESET, request_body)

def make_email_confirmation_post(confirmation_token: str, token_type: str) -> tuple:
    request_body = construct_request_body(confirmation_token, token_type, endpoint_constants.CONFIRMATION)
    return send_notification_request(endpoint_constants.EMAIL_CONFIRMATION, request_body)

def send_notification_request(notification_endpoint: str, request_body: dict) -> tuple:
    response = requests.post(endpoint_constants.NOTIFICATION_MS_URL + notification_endpoint, json=request_body)
    return_content = None

    match response.status_code:
        case 200:
            # Email confirmation has been sent successfully
            return_content = dict(renderModalTemplate = render_template(template_constants.MODAL_NOTIFICATION_SENT_PATH))
        case _:
            # Email delivery failure
            return_content = dict(url = request.referrer)
            print("Error occured: " + str(response.json()))
            pass

    return return_content, response.status_code

def construct_request_body(confirmation_token: str, token_type: str, target_endpoint: str) -> dict:
    form_details = request.form
    endpoint_parameters = f"{target_endpoint}?token={confirmation_token}&type={token_type}%20"
    target_url = urljoin(request.url_root, endpoint_parameters)
    return dict(targetUrl=target_url, recipient=form_details["username"])