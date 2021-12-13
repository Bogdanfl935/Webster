from flask import Flask, jsonify, request
from app.crawling_service import do_crawling, get_next_link, get_config, get_last_crawled, stop_crawling
from app.config import app
from werkzeug.exceptions import HTTPException
from app.error_handler import ErrorHandler
import endpoint_constants
import constants
import app_constants
import asyncio
import time
from datetime import datetime


@app.route(endpoint_constants.CRAWLER, methods=['POST'])
def handle_crawler_post() -> str:
    text = request.json.get(constants.START_LINK_KEY, None)
    # crawled_response = do_crawling(text)

    asyncio.run(do_crawling(text))
    # asyncio.run(do_crawling(text))

    return ('', 200)


@app.route(endpoint_constants.CRAWLER, methods=['GET'])
def handle_crawler_get() -> str:
    username = request.args.get("username")
    return get_last_crawled(username)


@app.route(endpoint_constants.STOP_CRAWLING, methods=['GET'])
def handle_stop_crawling_get() -> str:
    return stop_crawling()


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
