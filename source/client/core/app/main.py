from flask import Flask, jsonify, render_template
from app.constants import app_constants, endpoint_constants, rendering_constants, template_constants, static_constants
from werkzeug.exceptions import HTTPException
import random

app = Flask(__name__)


@app.context_processor
def inject_constants():
    return dict(
        static_constants=static_constants,
        template_constants=template_constants,
        home_endpoint=in_post_link.__name__,
        data_crawled_endpoint=handle_data_crawled.__name__
    )


@app.errorhandler(Exception)
def handle_error(exception):
    error_code = exception.code if isinstance(exception, HTTPException) else 500
    error_dict = dict(
        error_status=error_code,
        error_message=str(exception)
    )
    return render_template(template_constants.ERROR_ERROR_PATH, error=error_dict)


@app.route(endpoint_constants.DEFAULT, methods=['GET'])
@app.route(endpoint_constants.HOME, methods=['GET'])
def in_post_link() -> str:
    return render_template(template_constants.SECTION_HOME_PATH, logged_in=True)


@app.route(endpoint_constants.CRAWLED_CONTENT, methods=['GET'])
def handle_data_crawled() -> str:
    content_list = list()
    hosts = ("Github", "Google", "Wikipedia", "Youtube", "Jira", "Facebook", "Instagram")
    for i in range(0, 15):
        content_list.append({
            "page_host": random.choice(hosts),
            "time_taken": random.randint(1, 30),
            "quantity_found": random.randint(1, 100),
        })

    return render_template(template_constants.SECTION_CRAWLED_CONTENT_PATH, logged_in=False,
                           crawled_content_list=content_list)


if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
