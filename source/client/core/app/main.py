from flask import render_template, Response
from app.constants import app_constants, endpoint_constants, template_constants, static_constants, main_endpoint_handler_constants
from werkzeug.exceptions import HTTPException
from app.config.app_config import app
from app.service.authorization_service import require_access_token
import random, logging


@app.context_processor
def inject_constants() -> dict:
    return dict(
        static_constants=static_constants,
        template_constants=template_constants,
        home_endpoint=main_endpoint_handler_constants.HANDLE_HOME_GET,
        data_crawled_endpoint=main_endpoint_handler_constants.HANDLE_DATA_CRAWLED_GET
    )


@app.errorhandler(401)
def handle_unauthorized_error(exception: HTTPException) -> str:
    rendered_template = render_template(template_constants.SECTION_HOME_PATH)
    return rendered_template, exception.code


@app.errorhandler(Exception)
def handle_generic_error(exception) -> str:
    error_code = exception.code if isinstance(
        exception, HTTPException) else 500
    error_dict = dict(
        error_status=error_code,
        error_message=str(exception)
    )

    if error_code == 500:
        logging.exception(exception)

    return render_template(template_constants.INDIVIDUAL_ERROR_PATH, error=error_dict), error_code

@app.route(endpoint_constants.DEFAULT, methods=['GET'])
@app.route(endpoint_constants.HOME, methods=['GET'])
@require_access_token
def handle_home_get(response_object: Response, authenticated_user: str) -> str:
    response_object.set_data(
        render_template(
            template_constants.SECTION_HOME_PATH,
            authenticated_user=authenticated_user
        )
    )
    return response_object

@app.route(endpoint_constants.CRAWLED_CONTENT, methods=['GET'])
@require_access_token
def handle_data_crawled_get(response_object: Response, authenticated_user: str) -> str:
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
            template_constants.SECTION_CRAWLED_CONTENT_PATH,
            authenticated_user=authenticated_user,
            crawled_content_list=content_list
        )
    )
    return response_object


if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST,
            port=app_constants.APP_PORT, debug=True)
