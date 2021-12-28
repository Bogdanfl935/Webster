from flask import Flask, request, Response, make_response, jsonify
from app.constants import app_constants, endpoint_constants, constants
from app.services import config_service
from app.config.app_config import flask_app
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from app.validation import validation_schema
from app.services.validation_service import validate_with_schema, ValidationTarget
from http import HTTPStatus
import time, logging, traceback
from datetime import datetime


@flask_app.route(endpoint_constants.CONFIGURATION, methods=['POST'])
@validate_with_schema(validation_schema.AddConfigSchema)
def handle_config_post() -> str:
    return config_service.add_config_to_db(request)


@flask_app.route(endpoint_constants.CRAWLER_CONFIGURATION, methods=['GET'])
@validate_with_schema(validation_schema.RetriveConfigSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_crawler_config_get() -> str:
    return config_service.retr_config_from_db(request, constants.CRAWLER_LABEL)


@flask_app.route(endpoint_constants.PARSER_CONFIGURATION, methods=['GET'])
@validate_with_schema(validation_schema.RetriveConfigSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_parser_config_get() -> str:
    return config_service.retr_config_from_db(request, constants.PARSER_LABEL)


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
    flask_app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
