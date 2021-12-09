from flask import Flask, jsonify, request
from app.crawling_service import do_crawling, get_next_link, get_config, get_last_crawled
import endpoint_constants
import constants
import app_constants
import asyncio

app = Flask(__name__)

@app.route(endpoint_constants.CRAWLER, methods=['POST'])
def in_post_link() -> str:
    text = request.json.get(constants.START_LINK_KEY, None)
    # crawled_response = do_crawling(text)

    asyncio.run(do_crawling(text))
    # asyncio.run(do_crawling(text))


    return ('', 200)
        
@app.route(endpoint_constants.CRAWLER, methods=['GET'])
def in_get_data() -> str:
    resp = get_last_crawled()
    return jsonify({"last_link": resp})

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)