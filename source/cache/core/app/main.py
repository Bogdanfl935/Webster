from http import HTTPStatus
from flask import jsonify, Response, make_response, request
from app.constants import endpoint_constants, app_constants
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import memory_usage_service, concurrent_status_service, concurrent_continuation_service, \
    last_url_service
from app.dto.error_handler import ErrorHandler
from app.config.app_config import flask_app
from app.validation import validation_schema
from werkzeug.exceptions import HTTPException
import time
from datetime import datetime


@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['POST'])
@validate_with_schema(validation_schema.MemoryUsageSchema)
def handle_memory_usage_post() -> Response:
    return memory_usage_service.set_memory_usage()


@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_memory_usage_get() -> Response:
    return memory_usage_service.get_memory_usage()


@flask_app.route(endpoint_constants.STATUS, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_status_get() -> Response:
    return concurrent_status_service.get_active_status()


@flask_app.route(endpoint_constants.CONCURRENT_STATUS_READING, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_concurrent_status_reading_post() -> Response:
    return concurrent_status_service.get_and_set_active_status()


@flask_app.route(endpoint_constants.CONCURRENT_STATUS_WRITING, methods=['POST'])
@validate_with_schema(validation_schema.ConcurrentWritingSchema)
def handle_concurrent_status_writing_post() -> Response:
    return concurrent_status_service.set_active_status()


@flask_app.route(endpoint_constants.CONCURRENT_CONTINUATION_READING, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_concurrent_continuation_reading_post() -> Response:
    return concurrent_continuation_service.get_and_set_continuation_status()


@flask_app.route(endpoint_constants.CONCURRENT_CONTINUATION_WRITING, methods=['POST'])
@validate_with_schema(validation_schema.ConcurrentContinuationWritingSchema)
def handle_concurrent_continuation_writing_post() -> Response:
    return concurrent_continuation_service.set_continuation_status()


@flask_app.route(endpoint_constants.LAST_URL, methods=['POST'])
@validate_with_schema(validation_schema.LastUrlSchema)
def handle_last_url_post() -> Response:
    return last_url_service.set_last_url()


@flask_app.route(endpoint_constants.LAST_URL, methods=['GET'])
def handle_last_url_get() -> Response:
    return last_url_service.get_last_url()


@flask_app.errorhandler(400)
def handle_bad_request_error(exception: HTTPException) -> Response:
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code,
                            error=HTTPStatus(exception.code).phrase,
                            errors=exception.description, path=request.path)
    return make_response(jsonify(exception_dto.__dict__), exception.code)


@flask_app.errorhandler(Exception)
def handle_generic_error(exception) -> Response:
    error_code = exception.code if isinstance(exception, HTTPException) else HTTPStatus.INTERNAL_SERVER_ERROR
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=error_code,
                            error=HTTPStatus(exception.code).phrase,
                            message=str(exception), path=request.path)
    return make_response(jsonify(exception_dto.__dict__), error_code)


if __name__ == '__main__':
    flask_app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
