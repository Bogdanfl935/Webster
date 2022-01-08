from app.service.validation_service import ValidationTarget, validate_with_schema
from app.constants import endpoint_constants
from app.config.env_config import APP_HOST, APP_PORT
from flask import jsonify, make_response, request, Response
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from app.validation import validation_schema
from app.service import crawling_service, executor_service
from app.config.app_config import app
from http import HTTPStatus
from datetime import datetime
import time, logging, traceback


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
    return crawling_service.get_crawler_status()

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
    if error_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        logging.log(level=logging.DEBUG, msg=traceback.format_exc())
    return make_response(jsonify(exception_dto.__dict__), error_code)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
    executor_service.shutdown()
