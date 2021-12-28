from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.user_mapping_service import fetch_user_id
from flask import request, make_response, jsonify
from http import HTTPStatus



def get_memory_limit():
    # User ID is not used as memory limit is not distinguished between users
    # If different memory limits are introduced for users, the User ID may
    # be used to fetch associated memory limit (i.e. according to their account
    # status perks)
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    query_func = lambda session: session.query(sql_models.MemoryLimit).value(sql_models.MemoryLimit.capacity)
    record = persistence_service.query(query_func)
    response = {serialization_constants.MEMORY_LIMIT_KEY: record}

    return make_response(jsonify(response), HTTPStatus.OK)