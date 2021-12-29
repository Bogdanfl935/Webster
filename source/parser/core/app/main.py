from app.service.validation_service import ValidationTarget, validate_with_schema
from flask import jsonify, make_response, request, Response
from app.constants import endpoint_constants, app_constants
from app.config.queue_config import AMQP_QUEUE
from app.validation import validation_schema
from app.dto.error_handler import ErrorHandler
from werkzeug.exceptions import HTTPException
from app.service import parsing_service, queue_consumer_service
from app.config.app_config import app
from http import HTTPStatus
from datetime import datetime
import time, logging, traceback



@app.route(endpoint_constants.PARSER_STATUS, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_parser_status_get() -> str:
    return parsing_service.get_last_parsed_content()

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
    queue_consumer_service.subscribe(AMQP_QUEUE)
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT)
    queue_consumer_service.shutdown()