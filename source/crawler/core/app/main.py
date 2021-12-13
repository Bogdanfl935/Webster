from flask import Flask, jsonify, request
from app.crawling_service import do_crawling, get_next_link, get_config, get_last_crawled, stop_crawling
from app.config import app
from werkzeug.exceptions import HTTPException
from app.error_handler import ErrorHandler
import endpoint_constants
import constants
import app_constants
import asyncio


@app.route(endpoint_constants.CRAWLER_START, methods=['POST'])
def handle_crawler_start_post() -> str:
    text = request.json.get(constants.START_LINK_KEY, None)
    print(request.json)
    # crawled_response = do_crawling(text)

    asyncio.run(do_crawling(text))
    # asyncio.run(do_crawling(text))

    return ('', 200)


@app.route(endpoint_constants.CRAWLER_STATUS, methods=['GET'])
def handle_crawler_status_get() -> str:
    username = request.args.get("username")
    return get_last_crawled(username)

@app.route(endpoint_constants.CRAWLER_STOP, methods=['POST'])
def handle_crawler_stop_post() -> str:
    return stop_crawling()

@app.errorhandler(401)
def handle_unauthorized_error(exception: HTTPException) -> str:
    myError = ErrorHandler()
    return json.dumps(myError.__dict__)

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)
