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

    specific_tag = "a"
    stay_on_same_page = "False"
    storage_limit = "100"

    if "specific-tag" in text.keys():
        specific_tag = text["specific-tag"]

    if "same-page" in text.keys():
        stay_on_same_page = text["same-page"]

    if "storage-limit" in text.keys():
        storage_limit = text["storage-limit"]

    config_json = jsonify({"specific-tag": specific_tag, "same-page": stay_on_same_page, "storage-limit": storage_limit})

    post_to_db = requests.post(url = f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.STORE_CONFIGURATION}', data=config_json, headers={'Content-type': 'application/json'})

    return config_json

@app.route(endpoint_constants.RETRIEVE_CONFIGURATION_CONFIG, methods=['POST'])
def handle_config_get() -> str:
    retr_config_req = jsonify(user="george")
    from_db_resp = requests.post(url = f'{endpoint_constants.STORAGE_MS_URL}{endpoint_constants.RETRIEVE_CONFIGURATION_DB}', data=retr_config_req, headers={'Content-type': 'application/json'}

    from_db_resp = from_db_resp.get_json()

    return from_db_resp

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)