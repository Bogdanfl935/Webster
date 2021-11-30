import requests
from flask import Flask, jsonify, request
import endpoint_constants
import constants
import app_constants
from werkzeug.utils import environ_property

app = Flask(__name__)

@app.route(endpoint_constants.CONFIGURATION, methods=['POST'])
def handle_config_post() -> str:
    text = request.get_json()

    specific_tag = ["a"]
    stay_on_same_page = False if "same-page" not in text else text["same-page"]
    storage_limit = 100 if "storage-limit" not in text else text["storage-limit"]

    if "specific-tag" in text.keys():
        specific_tag.append(text["specific-tag"])

    config_json = jsonify({"specific-tag": specific_tag, "same-page": stay_on_same_page, "storage-limit": storage_limit})

    # post_to_db = requests.post(url = f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.STORE_CONFIGURATION}', data=config_json, headers={'Content-type': 'application/json'})

    return config_json

@app.route(endpoint_constants.RETRIEVE_CONFIGURATION_CONFIG, methods=['POST'])
def handle_config_get() -> str:
    retr_config_req = jsonify(user="george")

    from_db_resp = requests.post(url = f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.RETRIEVE_CONFIGURATION_DB}', data=retr_config_req, headers={'Content-type': 'application/json'})

    from_db_resp_json = from_db_resp.json()

    return from_db_resp_json

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)