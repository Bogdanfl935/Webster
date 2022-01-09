from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.foreign_key_mapping_service import fetch_user_id
from flask import request, make_response, jsonify, Response
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

def get_memory_usage():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    query_func = lambda session: session.query(sql_models.MemoryUsage.usage).filter(
        sql_models.MemoryUsage.user_id == user_id).one_or_none()
    record = persistence_service.query(query_func)
    response = {serialization_constants.MEMORY_USAGE_KEY: record.usage if record is not None else 0}

    return make_response(jsonify(response), HTTPStatus.OK)

def update_memory_usage():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    memory_usage = request.json.get(serialization_constants.MEMORY_USAGE_KEY)
    fetch_query_func = lambda session: session.query(sql_models.MemoryUsage).filter(
        sql_models.MemoryUsage.user_id == user_id).one_or_none()
    existing_usage_record = persistence_service.query(fetch_query_func)

    if existing_usage_record is not None:
        record_model = sql_models.MemoryUsage(id=existing_usage_record.id, user_id=user_id, usage=memory_usage)
    else:
        record_model = sql_models.MemoryUsage(user_id=user_id, usage=memory_usage)

    query_func = lambda session: session.merge(record_model)
    persistence_service.query(query_func)
    persistence_service.commit_session()

    return Response(status=HTTPStatus.OK)