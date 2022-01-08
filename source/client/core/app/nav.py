from flask import render_template, Response, Blueprint
from app.constants import endpoint_constants, template_constants, nav_endpoint_handler_constants
from app.service import activity_service, config_service
from app.service.authorization_service import require_access_token
import random

nav = Blueprint('nav', __name__)


@nav.app_context_processor
def inject_context_constants() -> dict:
    return dict(
        home_endpoint=nav_endpoint_handler_constants.HANDLE_HOME_GET,
        activity_endpoint=nav_endpoint_handler_constants.HANDLE_ACTIVITY_GET,
        config_endpoint=nav_endpoint_handler_constants.HANDLE_CONFIG_GET,
        archive_endpoint=nav_endpoint_handler_constants.HANDLE_ARCHIVE_GET
    )

@nav.route(endpoint_constants.DEFAULT, methods=['GET'])
@nav.route(endpoint_constants.HOME, methods=['GET'])
@require_access_token
def handle_home_get(response_object: Response, authenticated_user: str) -> str:
    response_object.set_data(
        render_template(
            template_constants.SECTION_HOME_PATH,
            authenticated_user=authenticated_user
        )
    )
    return response_object

@nav.route(endpoint_constants.ACTIVITY, methods=['GET'])
@require_access_token
def handle_activity_get(response_object: Response, authenticated_user: str) -> Response:
    return activity_service.get_crawler_activity(response_object, authenticated_user)

@nav.route(endpoint_constants.CONFIGURATION, methods=['GET'])
@require_access_token
def handle_config_get(response_object: Response, authenticated_user: str) -> str:
    return config_service.render_configuration(response_object, authenticated_user)

@nav.route(endpoint_constants.ARCHIVE, methods=['GET'])
@require_access_token
def handle_archive_get(response_object: Response, authenticated_user: str) -> str:
    content_list = list()
    hosts = ("Github", "Google", "Wikipedia",
             "Youtube", "Jira", "Facebook", "Instagram")
    for i in range(0, 15):
        content_list.append({
            "page_host": random.choice(hosts),
            "time_taken": random.randint(1, 30),
            "quantity_found": random.randint(1, 100),
        })
    response_object.set_data(
        render_template(
            template_constants.SECTION_ARCHIVE_PATH,
            authenticated_user=authenticated_user,
            crawled_content_list=content_list
        )
    )
    return response_object
