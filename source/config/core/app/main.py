from flask import Flask, jsonify, request
import endpoint_constants
import constants
import app_constants

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

    return jsonify({"specific-tag": specific_tag, "same-page": stay_on_same_page, "storage-limit": storage_limit})

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)