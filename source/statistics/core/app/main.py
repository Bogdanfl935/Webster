from flask import Response, request, make_response, jsonify
from app.constants import endpoint_constants
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.validation import validation_schema
from werkzeug.exceptions import HTTPException
from app.config.app_config import app
from app.config.env_config import APP_HOST, APP_PORT
import logging, time, traceback
from datetime import datetime
from http import HTTPStatus
from app.dto.error_handler import ErrorHandler
from app.services import parsed_content_service


@app.route(endpoint_constants.STATISTICS_PUBLIC_CHART, methods=['GET'])
def handle_public_stats_chart_get():
    return parsed_content_service.get_content_public()


@app.route(endpoint_constants.STATISTICS_PRIVATE_CHART, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_private_stats_chart_get():
    return parsed_content_service.get_content_private()

@app.route(endpoint_constants.STATISTICS_PUBLIC, methods=['GET'])
def handle_public_stats_get():
    mem_usage = parsed_content_service.get_mem_usage_public()
    visited_urls = parsed_content_service.get_visited_urls_public()
    total_parsed_urls = parsed_content_service.get_total_parsed_urls_public()

    return jsonify(memoryUsage=mem_usage, visitedUrls=visited_urls, totalParsedUrls=total_parsed_urls)


@app.route(endpoint_constants.STATISTICS_PRIVATE, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_private_stats_get():
    mem_usage = parsed_content_service.get_mem_usage_private()
    visited_urls = parsed_content_service.get_visited_urls_private()
    total_parsed_urls = parsed_content_service.get_total_parsed_urls_private()

    return jsonify(memoryUsage=mem_usage, visitedUrls=visited_urls, totalParsedUrls=total_parsed_urls)



@app.errorhandler(HTTPStatus.BAD_REQUEST)
def handle_bad_request_error(exception: HTTPException) -> Response:
    exception_dto = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code,
                            error=HTTPStatus(exception.code).phrase,
                            errors=exception.description, path=request.path)
    return make_response(jsonify(exception_dto.__dict__), exception.code)


@app.errorhandler(Exception)
def handle_generic_error(exception) -> str:
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
