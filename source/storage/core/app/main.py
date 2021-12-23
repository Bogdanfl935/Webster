from flask import request, jsonify, Response, make_response
from app.constants import app_constants, endpoint_constants
from app.services import config_service, storage_access_service
from app.config.app_config import flask_app
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.dto.error_handler import ErrorHandler
from app.validation import validation_schema
from http import HTTPStatus
import time
from datetime import datetime

# users = User.query.all()

@flask_app.route(endpoint_constants.STORAGE, methods=['POST'])
@validate_with_schema(validation_schema.AddingUrlsSchema)
def handle_storage_post() -> str:
    return storage_access_service.add_link_to_db(request)

@flask_app.route(endpoint_constants.NEXT_LINK, methods=['POST'])
@validate_with_schema(validation_schema.NextUrlsSchema)
def handle_next_link_post() -> str:
    return storage_access_service.get_next_links(request)

@flask_app.route(endpoint_constants.STORE_CONFIGURATION, methods=['POST'])
@validate_with_schema(validation_schema.StoreConfigSchema)
def handle_store_config_post() -> str:
    return config_service.add_new_config_to_db(request)

@flask_app.route(endpoint_constants.RETR_CONFIGURATION, methods=['POST'])
@validate_with_schema(validation_schema.RetrieveConfigSchema)
def handle_retr_config_post() -> str:
    return config_service.get_config_from_db(request)

@flask_app.route(endpoint_constants.PARSED_CONTENT, methods=['POST'])
@validate_with_schema(validation_schema.ParsedDataSchema)
def handle_parsed_content_post() -> str:
    return jsonify({})

@flask_app.route(endpoint_constants.PARSED_IMAGES, methods=['POST'])
@validate_with_schema(validation_schema.ParsedDataSchema)
def handle_parsed_images_post() -> str:
    return jsonify({})

@flask_app.errorhandler(HTTPStatus.BAD_REQUEST)
def handle_bad_request_error(exception: HTTPException) -> Response:
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code,
                            error=HTTPStatus(exception.code).phrase,
                            errors=exception.description, path=request.path)
    return make_response(jsonify(exception_dto.__dict__), exception.code)


@flask_app.errorhandler(Exception)
def handle_generic_error(exception) -> Response:
    error_code = exception.code if isinstance(exception, HTTPException) else HTTPStatus.INTERNAL_SERVER_ERROR
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=error_code,
                            error=HTTPStatus(error_code).phrase,
                            message=str(exception), path=request.path)
    return make_response(jsonify(exception_dto.__dict__), error_code)


if __name__ == '__main__':
    flask_app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)