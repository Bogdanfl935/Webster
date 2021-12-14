from flask import Flask, request
from app.constants import app_constants, endpoint_constants, constants
from app import config_service

app = Flask(__name__)

@app.route(endpoint_constants.CONFIGURATION, methods=['POST'])
def handle_config_post() -> str:
    return config_service.add_config_to_db(request)

@app.route(endpoint_constants.CRAWLER_CONFIGURATION, methods=['GET'])
def handle_crawler_config_get() -> str:
    return config_service.retr_config_from_db(request, constants.CRAWLER_LABEL)

@app.route(endpoint_constants.PARSER_CONFIGURATION, methods=['GET'])
def handle_parser_config_get() -> str:
    return config_service.retr_config_from_db(request, constants.PARSER_LABEL)

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)