from flask import render_template, Response
from app.constants import template_constants
from app.service import crawler_service, parser_service, config_service
import json

def get_crawler_activity(response_object: Response, authenticated_user: str) -> Response:
    crawler_latest_status, _ = crawler_service.make_status_get(authenticated_user)
    crawler_config, _ = config_service.make_crawler_config_get(authenticated_user)
    
    if crawler_latest_status["active"] is True:
        parser_latest_status = parser_service.make_status_get(authenticated_user)
        response_object.set_data(
            render_template(
                template_constants.SECTION_ACTIVITY_ACTIVE_PATH,
                authenticated_user = authenticated_user,
                crawler_status = crawler_latest_status,
                parser_status = parser_latest_status,
                memory_limit = int(crawler_config["memoryLimit"]) # To be fixed later
            )
        )
    else:
        response_object.set_data(
            render_template(
                template_constants.SECTION_ACTIVITY_INACTIVE_PATH,
                authenticated_user = authenticated_user,
                crawler_status = crawler_latest_status,
                memory_limit = int(crawler_config["memoryLimit"]) # To be fixed later
            )
        )
        
    return response_object

def get_crawler_status(response_object: Response, authenticated_user: str) -> Response:
    crawler_latest_status, _ = crawler_service.make_status_get(authenticated_user)
    response_object.set_data(json.dumps(crawler_latest_status).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object

def get_parser_status(response_object: Response, authenticated_user: str) -> Response:
    crawler_latest_status, _ = parser_service.make_status_get(authenticated_user)
    response_object.set_data(json.dumps(crawler_latest_status).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object

def start_crawling(response_object: Response, authenticated_user: str) -> Response:
    crawler_service.make_crawler_start_post(authenticated_user)
    return response_object

def stop_crawling(response_object: Response, authenticated_user: str) -> Response:
    crawler_service.make_crawler_stop_post(authenticated_user)
    return response_object