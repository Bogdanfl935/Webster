from flask import render_template, Response
from app.constants import template_constants
from app.service import crawler_service, parser_service, config_service

def get_crawler_activity(response_object: Response, authenticated_user: str) -> Response:
    crawler_latest_status = crawler_service.make_status_get(authenticated_user)
    general_config = config_service.make_general_config_get(authenticated_user)
    
    if crawler_latest_status["active"] is True:
        parser_latest_status = parser_service.make_status_get(authenticated_user)
        response_object.set_data(
            render_template(
                template_constants.SECTION_ACTIVITY_ACTIVE_PATH,
                authenticated_user = authenticated_user,
                crawler_status = crawler_latest_status,
                parser_status = parser_latest_status,
                memory_limit = general_config["memoryLimit"]
            )
        )
    else:
        response_object.set_data(
            render_template(
                template_constants.SECTION_ACTIVITY_INACTIVE_PATH,
                authenticated_user = authenticated_user,
                crawler_status = crawler_latest_status,
                memory_limit = general_config["memoryLimit"]
            )
        )
        
    return response_object