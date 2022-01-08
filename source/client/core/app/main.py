from flask import render_template, request, make_response, jsonify
from app.constants import template_constants, static_constants
from werkzeug.exceptions import HTTPException
from app.config.app_config import app
from app.config.env_config import APP_HOST, APP_PORT
import logging, time, traceback
from datetime import datetime
from http import HTTPStatus
from app.dto.error_handler import ErrorHandler


@app.context_processor
def inject_constants() -> dict:
    return dict(
        static_constants=static_constants,
        template_constants=template_constants
    )


@app.errorhandler(401)
def handle_unauthorized_error(exception: HTTPException) -> str:
    rendered_template = render_template(template_constants.SECTION_HOME_PATH)
    return rendered_template, exception.code


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
