from app.service.validation_service import ValidationTarget, validate_with_schema
from app.constants import endpoint_constants, app_constants
from flask import jsonify, make_response, request, Response
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from app.validation import validation_schema
from app.service import crawling_service
from app.config import app
from http import HTTPStatus
from datetime import datetime
import time


@app.route(endpoint_constants.CRAWLER_START, methods=['POST'])
@validate_with_schema(validation_schema.StartCrawlerSchema)
def handle_crawler_post():
    return crawling_service.start_crawling()

@app.route(endpoint_constants.CRAWLER_STOP, methods=['POST'])
@validate_with_schema(validation_schema.UsernameAccessSchema)
def handle_crawler_stop_post():
    return crawling_service.stop_crawling()

@app.route(endpoint_constants.CRAWLER_STATUS, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_crawler_status_get():
    return crawling_service.get_last_crawled_url()

@app.errorhandler(HTTPStatus.BAD_REQUEST)
def handle_bad_request_error(exception: HTTPException) -> Response:
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code,
                            error=HTTPStatus(exception.code).phrase,
                            errors=exception.description, path=request.path)
    return make_response(jsonify(exception_dto.__dict__), exception.code)


@app.errorhandler(Exception)
def handle_generic_error(exception) -> Response:
    error_code = exception.code if isinstance(exception, HTTPException) else HTTPStatus.INTERNAL_SERVER_ERROR
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=error_code,
                            error=HTTPStatus(error_code).phrase,
                            message=str(exception), path=request.path)
    return make_response(jsonify(exception_dto.__dict__), error_code)


if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
