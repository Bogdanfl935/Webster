from http import HTTPStatus
from flask import jsonify, Response, make_response, request
from app.constants import endpoint_constants, app_constants
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import memory_usage_service
from app.dto.error_handler import ErrorHandler
from app.config.app_config import flask_app
from app.validation import validation_schema
from werkzeug.exceptions import HTTPException
import time
from datetime import datetime


@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['POST'])
@validate_with_schema(validation_schema.MemoryUsageSchema)
def handle_memory_usage_post() -> Response:
    return memory_usage_service.increase_memory_usage()


@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_memory_usage_get() -> Response:
    return memory_usage_service.get_memory_usage()



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
