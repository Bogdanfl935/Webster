from flask import Flask, jsonify, request
from app.find_links import parsing_service, get_last_parsed
from app.config import app
import endpoint_constants
import constants
import app_constants
from werkzeug.exceptions import HTTPException
from app.error_handler import ErrorHandler
import time
from datetime import datetime

@app.route(endpoint_constants.PARSER, methods=['POST'])
def handle_parser_post() -> str:
    text = request.json.get(constants.CONTENT_KEY, None)
    url = request.json.get(constants.URL_KEY, None)
    # text = request.data.decode()

    # get links from the webpage
    next_urls = parsing_service(text, url)

    return next_urls

@app.route(endpoint_constants.PARSER, methods=['GET'])
def handle_parser_get() -> str:
    username = request.args.get('username')

    return get_last_parsed(username)

@app.errorhandler(400)
def handle_unauthorized_error(exception: HTTPException) -> str:
    myError = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=exception.code, error="Bad Request",
                           errors=[exception.description])
    return jsonify(myError.__dict__)


@app.errorhandler(Exception)
def handle_generic_error(exception) -> str:
    error_code = exception.code if isinstance(
        exception, HTTPException) else 500

    path = exception.request.path_url if isinstance(
        exception, HTTPException) else None

    myError = ErrorHandler(timestamp=datetime.fromtimestamp(time.time()), status=error_code, error="Internal Server Error",
                           message=str(exception), path=path)
    return jsonify(myError.__dict__)

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)