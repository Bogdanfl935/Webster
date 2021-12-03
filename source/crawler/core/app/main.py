from flask import Flask, jsonify, request
from app.crawling_service import do_crawling, get_next_link, get_config
import endpoint_constants
import constants
import app_constants

app = Flask(__name__)

@app.route(endpoint_constants.CRAWLER, methods=['POST'])
def in_post_link() -> str:
    text = request.json.get(constants.START_LINK_KEY, None)

    json_config = get_config()

    max_total_size = int(json_config["storage-limit"][0])
    max_total_size = max_total_size * 10 ** 6

    next_urls = jsonify({"urls": []})

    # in do_crawling we do a POST on /parser
    crawled_size = do_crawling(text)
    while crawled_size < max_total_size:
        if crawled_size == -1:
            next_urls = get_next_link()
            for el in next_urls["urls"]:
                crawled_size = do_crawling(el)
        else:
            max_total_size = max_total_size - crawled_size
            next_urls = get_next_link()
            for el in next_urls["urls"]:
                crawled_size = do_crawling(el)

    return next_urls
        
@app.route(endpoint_constants.CRAWLER, methods=['GET'])
def in_get_data() -> str:
    return jsonify({"ala": "bala"})

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)