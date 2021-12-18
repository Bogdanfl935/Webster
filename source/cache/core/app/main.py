from app.constants import endpoint_constants, app_constants
from app.services import memory_usage_service, concurrent_status_service, concurrent_continuation_service, \
    last_url_service
from flask import jsonify, request, Response
from app.config.app_config import flask_app
from werkzeug.exceptions import HTTPException
from requests.exceptions import ConnectionError
from app.dto.error_handler import ErrorHandler
import app.constants
import time
from datetime import datetime
from app.services.validation_service import validate_schema
from app.validation import validation_schema
from http import HTTPStatus


@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['POST'])
@validate_schema(validation_schema.MemoryUsageSchema)
def handle_memory_usage_post() -> Response:
    username = request.json.get("username", None)
    memory_usage = request.json.get("memoryUsage", None)

    memory_usage_service.modify_memory_usage(username, memory_usage)

    return Response(status=HTTPStatus.OK)


@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['GET'])
def handle_memory_usage_get() -> dict:
    username = request.args.get("username")

    return memory_usage_service.get_memory_usage(username)


@flask_app.route(f'{endpoint_constants.MEMORY_USAGE}{endpoint_constants.STATUS}', methods=['GET'])
def handle_status_get() -> dict:
    username = request.args.get("username")

    return concurrent_status_service.get_active_status(username)


@flask_app.route(endpoint_constants.CONCURRENT_STATUS_READING, methods=['POST'])
@validate_schema(validation_schema.ConcurrentReadingSchema)
def handle_concurrent_status_reading_post() -> dict:
    username = request.json.get("username", None)

    return concurrent_status_service.get_active_status(username)


@flask_app.route(endpoint_constants.CONCURRENT_STATUS_WRITING, methods=['POST'])
@validate_schema(validation_schema.ConcurrentWritingSchema)
def handle_concurrent_status_writing_post() -> Response:
    username = request.json.get("username", None)
    active = request.json.get("active", None)

    concurrent_status_service.set_active_status(username, active)

    return Response(status=HTTPStatus.OK)


@flask_app.route(endpoint_constants.CONCURRENT_CONTINUATION_READING, methods=['POST'])
@validate_schema(validation_schema.ConcurrentReadingSchema)
def handle_concurrent_continuation_reading_post() -> dict:
    username = request.json.get("username", None)

    return concurrent_continuation_service.get_continuation_status(username)


@flask_app.route(endpoint_constants.CONCURRENT_CONTINUATION_WRITING, methods=['POST'])
@validate_schema(validation_schema.ConcurrentContinuationWritingSchema)
def handle_concurrent_continuation_writing_post() -> Response:
    username = request.json.get("username", None)
    continuation = request.json.get("continuation", None)

    concurrent_continuation_service.set_continuation_status(username, continuation)

    return Response(status=HTTPStatus.OK)


@flask_app.route(endpoint_constants.LAST_URL, methods=['POST'])
@validate_schema(validation_schema.LastUrlSchema)
def handle_last_url_post() -> Response:
    username = request.json.get("username", None)
    last_url = request.json.get("lastUrl", None)

    last_url_service.set_last_url(username, last_url)

    return Response(status=HTTPStatus.OK)


@flask_app.route(endpoint_constants.LAST_URL, methods=['GET'])
def handle_last_url_get() -> Response:
    username = request.args.get("username")

    return last_url_service.get_last_url(username)


@flask_app.errorhandler(400)
def handle_unauthorized_error(exception: HTTPException) -> Response:
    my_error = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code,
                            error="Bad Request",
                            errors=exception.description)
    return jsonify(my_error.__dict__)


@flask_app.errorhandler(Exception)
def handle_generic_error(exception) -> Response:
    error_code = exception.code if isinstance(
        exception, HTTPException) else 500

    if isinstance(exception, ConnectionError):
        path = exception.request.path_url
    else:
        path = None

    my_error = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=error_code,
                            error="Internal Server Error",
                            message=str(exception), path=path)
    return jsonify(my_error.__dict__)


if __name__ == '__main__':
    flask_app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
