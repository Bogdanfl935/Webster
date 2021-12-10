from flask import Flask, jsonify, request
from app.find_links import parsing_service, get_last_parsed
import endpoint_constants
import constants
import app_constants

app = Flask(__name__)

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
    return get_last_parsed()

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)