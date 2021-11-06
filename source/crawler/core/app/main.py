from flask import Flask, jsonify, request
from app.crawl_from_url import do_crawling
import endpoint_constants
import constants

app = Flask(__name__)

@app.route(endpoint_constants.CRAWLER, methods=['POST'])
def in_post_link() -> str:
    text = request.json.get(constants.START_LINK_KEY, None)

    # in do_crawling we do a POST on /parser
    next_urls = do_crawling(text)
    # resp = {"nextLink": next_urls}

    # return jsonify({"ana": "mere"})
    return next_urls
        
@app.route(endpoint_constants.CRAWLER, methods=['GET'])
def in_get_data() -> str:
    return jsonify({"ala": "bala"})

if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)