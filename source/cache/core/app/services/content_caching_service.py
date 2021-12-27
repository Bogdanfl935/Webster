from http import HTTPStatus
from app.constants import serialization_constants
from app.services.concurrent_access_service import acquire_lock, release_lock
from app.constants.lock_types import LockType
from app.constants import redis_constants
from app.config.redis_config import redis_last_url, redis_last_parsed
from flask import request, make_response, jsonify, Response
import json


def get_last_url():
    username = request.args.get(serialization_constants.USERNAME_KEY)
    last_url = redis_last_url.get(username).decode('utf-8') if redis_last_url.exists(username) != 0 else None
    return make_response(jsonify({serialization_constants.LAST_URL_KEY: last_url}), HTTPStatus.OK)


def set_last_url():
    username = request.json.get(serialization_constants.USERNAME_KEY)
    last_url = request.json.get(serialization_constants.LAST_URL_KEY)
    
    acquire_lock(LockType.LAST_URL_LOCK) # Enter critical section
    redis_last_url.set(username, last_url, ex=redis_constants.REDIS_LATEST_EXPIRATION)
    release_lock(LockType.LAST_URL_LOCK) # Exit critical section
    
    return Response(status=HTTPStatus.OK)


def get_last_parsed():
    username = request.args.get(serialization_constants.USERNAME_KEY)
    parsing_history = json.loads(redis_last_parsed.get(username).decode(
        'utf-8')) if redis_last_parsed.exists(username) != 0 else None
    response = make_response(jsonify(
        parsing_history), HTTPStatus.OK) if parsing_history is not None else Response(status=HTTPStatus.OK)
    return response


def set_last_parsed():
    username = request.json.get(serialization_constants.USERNAME_KEY)
    url = request.json.get(serialization_constants.URL_KEY)
    serialization_keys = (serialization_constants.TAG_KEY, serialization_constants.MEMORY_USAGE_KEY)
    filtered_request_dict = {key: request.json.get(key) for key in serialization_keys}

    acquire_lock(LockType.LAST_PARSED_LOCK)  # Enter critical section
    if redis_last_parsed.exists(username) != 0:
        parsing_history = json.loads(redis_last_parsed.get(username).decode('utf-8'))
        parsing_history[url] = parsing_history.get(url, []) + [filtered_request_dict]
    else:
        parsing_history = {url: [filtered_request_dict]}

    
    redis_last_parsed.set(username, json.dumps(parsing_history).encode(
            'utf-8'), ex=redis_constants.REDIS_LATEST_EXPIRATION)
    release_lock(LockType.LAST_PARSED_LOCK)  # Exit critical section

    return Response(status=HTTPStatus.OK)

