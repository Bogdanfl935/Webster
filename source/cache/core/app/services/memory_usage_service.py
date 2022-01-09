from http import HTTPStatus
from app.constants import serialization_constants
from app.config.redis_config import redis_memory_usage
from app.services import storage_service
from flask import request, make_response, jsonify, Response


def increase_memory_usage():
    username = request.json.get(serialization_constants.USERNAME_KEY)
    memory_usage = request.json.get(serialization_constants.MEMORY_USAGE_KEY)
    
    redis_memory_usage.incr(username, memory_usage)
    return Response(status=HTTPStatus.OK)


def get_memory_usage():
    username = request.args.get(serialization_constants.USERNAME_KEY)
    if redis_memory_usage.exists(username) != 0: # Get memory usage from cache
        memory_usage = int(redis_memory_usage.get(username).decode('utf-8'))
    else: # Get memory usage from storage
        memory_usage_response, _ = storage_service.make_memory_usage_get(username)
        memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
    return make_response(jsonify(dict(memoryUsage=memory_usage)), HTTPStatus.OK)
