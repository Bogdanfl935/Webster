from flask import Flask, jsonify, request
from app.crawling_service import do_crawling, get_next_link, get_config
import endpoint_constants
import constants
import app_constants

app = Flask(__name__)

@app.route(endpoint_constants.CRAWLER, methods=['POST'])
def in_post_link() -> str:
    text = request.json.get(constants.START_LINK_KEY, None)
    crawled_response = do_crawling(text)

    return crawled_response
        
@app.route(endpoint_constants.CRAWLER, methods=['GET'])
def in_get_data() -> str:
    return jsonify({"ala": "bala"})

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)