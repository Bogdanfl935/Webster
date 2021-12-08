from flask import render_template
from app.constants import app_constants, template_constants, static_constants
from werkzeug.exceptions import HTTPException
from app.config.app_config import app
import logging


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
    error_code = exception.code if isinstance(
        exception, HTTPException) else 500
    error_dict = dict(
        error_status=error_code,
        error_message=str(exception)
    )

    if error_code == 500:
        logging.exception(exception)

    return render_template(template_constants.INDIVIDUAL_ERROR_PATH, error=error_dict), error_code


if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST,
            port=app_constants.APP_PORT, debug=True)
