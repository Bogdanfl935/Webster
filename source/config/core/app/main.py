from flask import Flask, request, Response, make_response, jsonify
from app.constants import app_constants, endpoint_constants, constants
from app.services import config_service
from app.config.app_config import flask_app
from werkzeug.exceptions import HTTPException
from app.dto.error_handler import ErrorHandler
from app.validation import validation_schema
from http import HTTPStatus
import time, logging, traceback
from datetime import datetime


@flask_app.route(endpoint_constants.CONFIGURATION, methods=['POST'])
def handle_config_post() -> str:
    return config_service.add_config_to_db(request)


@flask_app.route(endpoint_constants.CRAWLER_CONFIGURATION, methods=['GET'])
def handle_crawler_config_get() -> str:
    return config_service.retr_config_from_db(request, constants.CRAWLER_LABEL)


@flask_app.route(endpoint_constants.PARSER_CONFIGURATION, methods=['GET'])
def handle_parser_config_get() -> str:
    return config_service.retr_config_from_db(request, constants.PARSER_LABEL)



if __name__ == '__main__':
    flask_app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
