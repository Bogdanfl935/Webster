from app.constants import endpoint_constants, main_endpoint_handler_constants
from flask import request, url_for
from app.utilities.url_joiner import urljoin
from app.utilities.api_response_parser import *
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
            return_content = dict(
                url=url_for(main_endpoint_handler_constants.HANDLE_HOME_GET),
                redirect=True
            )
        case _:
            # Email delivery failure
            return_content = dict(
                url=request.referrer,
                redirect=True
            )
            print("Error occured: " + str(response.json()))
            pass

    return return_content, response.status_code

def construct_request_body(confirmation_token: str, token_type: str, target_endpoint: str) -> dict:
    form_details = request.form
    endpoint_parameters = f"{target_endpoint}?token={confirmation_token}&type={token_type}%20"
    target_url = urljoin(request.url_root, endpoint_parameters)
    return dict(targetUrl=target_url, recipient=form_details["username"])