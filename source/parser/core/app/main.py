from flask import Flask, jsonify, request
from app.find_links import parse_urls
import endpoint_constants
import constants
import app_constants

app = Flask(__name__)

@app.route(endpoint_constants.PARSER, methods=['POST'])
def in_post_link() -> str:
    text = request.json.get(constants.CONTENT_KEY, None)

    # get links from the webpage
    next_urls = parse_urls(text)

    return next_urls;

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)