from flask import request, jsonify, Response, make_response
from app.constants import endpoint_constants
from app.services import storage_access_service
from app.config.app_config import flask_app
from app.config.env_config import APP_HOST, APP_PORT
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.dto.error_handler import ErrorHandler
from app.validation import validation_schema
from http import HTTPStatus
import time, logging, traceback
from datetime import datetime



@flask_app.route(endpoint_constants.MEMORY_LIMIT, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_memory_limit_get() -> Response:
    return storage_access_service.get_memory_limit()

@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_memory_usage_get() -> Response:
    return storage_access_service.get_memory_usage()

@flask_app.route(endpoint_constants.MEMORY_USAGE, methods=['PUT'])
@validate_with_schema(validation_schema.MemoryUsageSchema)
def handle_memory_usage_put() -> Response:
    return storage_access_service.update_memory_usage()

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
    if error_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        logging.log(level=logging.DEBUG, msg=traceback.format_exc())
    return make_response(jsonify(exception_dto.__dict__), error_code)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    flask_app.run(host=APP_HOST, port=APP_PORT, debug=True)
