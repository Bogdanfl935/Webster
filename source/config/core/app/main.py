from flask import request, Response, make_response, jsonify
from app.config.env_config import APP_HOST, APP_PORT
from app.config.app_config import flask_app
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from http import HTTPStatus
import time, logging, traceback
from datetime import datetime


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
