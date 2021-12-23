from flask import Flask, request, jsonify
from app.constants import app_constants, endpoint_constants
from app import config_service, storage_access_service
from app.config import app
from werkzeug.exceptions import HTTPException
from app.error_handler import ErrorHandler
import time
from datetime import datetime

# users = User.query.all()

@app.route(endpoint_constants.STORAGE, methods=['POST'])
def handle_storage_post() -> str:
    return storage_access_service.add_link_to_db(request)

@app.route(endpoint_constants.NEXT_LINK, methods=['POST'])
def handle_next_link_post() -> str:
    return storage_access_service.get_next_links(request)

@app.route(endpoint_constants.STORE_CONFIGURATION, methods=['POST'])
def handle_store_config_post() -> str:
    return config_service.add_new_config_to_db(request)

@app.route(endpoint_constants.RETR_CONFIGURATION, methods=['POST'])
def handle_retr_config_post() -> str:
    return config_service.get_config_from_db(request)

@app.route(endpoint_constants.PARSED_CONTENT, methods=['POST'])
def handle_parsed_content_post() -> str:
    return (200, '')

@app.route(endpoint_constants.PARSED_IMAGES, methods=['POST'])
def handle_parsed_images_post() -> str:
    return (200, '')

@app.errorhandler(400)
def handle_unauthorized_error(exception: HTTPException) -> str:
    myError = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code, error="Bad Request",
                           errors=[exception.description])
    return jsonify(myError.__dict__)


# @app.errorhandler(Exception)
# def handle_generic_error(exception) -> str:
#     error_code = exception.code if isinstance(
#         exception, HTTPException) else 500
#
#     path = exception.request.path_url if isinstance(
#         exception, HTTPException) else None
#
#     myError = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=error_code, error="Internal Server Error",
#                            message=str(exception), path=path)
#     return jsonify(myError.__dict__)


if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)