from flask import Flask, jsonify, request
from flask.wrappers import Request
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.crawl_from_url import do_crawling

app = Flask(__name__)

@app.route("/crawler", methods=['POST'])
def in_post_link() -> str:
    text = request.json.get("startLink", None)
     
    next_url = do_crawling(text)
    resp = {"nextLink": next_url}

    return jsonify(resp)
        
@app.route("/crawler", methods=['GET'])
def in_get_data() -> str:
    return jsonify({"ala": "bala"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  