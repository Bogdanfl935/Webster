from flask import Flask, request
from app.constants import app_constants, endpoint_constants, constants
from app import config_service

app = Flask(__name__)

@app.route(endpoint_constants.CONFIGURATION, methods=['POST'])
def handle_config_post() -> str:
    return config_service.add_config_to_db(request)

@app.route(endpoint_constants.RETRIEVE_CONFIGURATION_CRAWLER, methods=['POST'])
def handle_config_retr_crawler_post() -> str:
    return config_service.retr_config_from_db(request, constants.CRAWLER_LABEL)

@app.route(endpoint_constants.RETRIEVE_CONFIGURATION_PARSER, methods=['POST'])
def handle_config_retr_parser_post() -> str:
    return config_service.retr_config_from_db(request, constants.PARSER_LABEL)

if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)