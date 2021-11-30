from flask import Flask, request
from app.constants import app_constants, endpoint_constants
from app import config_service, storage_access_service
from app.config import app

# users = User.query.all()

@app.route(endpoint_constants.STORAGE, methods=['POST'])
def handle_storage_post() -> str:
    return storage_access_service.add_link_to_db(request)

@app.route(endpoint_constants.NEXT_LINK, methods=['POST'])
def handle_next_link_post() -> str:
    return storage_access_service.get_next_links(request)

@app.route(endpoint_constants.STORE_CONFIGURATION, methods=['POST'])
def handle_store_config_post() -> str:
    return config_service.add_new_config_to_db(request)

@app.route(endpoint_constants.RETR_CONFIGURATION, methods=['POST'])
def handle_retr_config_post() -> str:
    return config_service.get_config_from_db(request)


if __name__ == '__main__':
    app.run(host=app_constants.APP_HOST, port=app_constants.APP_PORT, debug=True)