from http import HTTPStatus

from app.config.redis_config import redis_memory_usage
from flask import request, make_response, jsonify, Response


def increase_memory_usage():
    username = request.json.get("username", None)
    memory_usage = request.json.get("memoryUsage", None)
    
    redis_memory_usage.incr(username, memory_usage)
    return Response(status=HTTPStatus.OK)


def get_memory_usage():
    username = request.args.get("username")
    memory_usage = int(redis_memory_usage.get(username).decode('utf-8')) if redis_memory_usage.exists(username) != 0 else 0
    return make_response(jsonify(dict(memoryUsage=memory_usage)), HTTPStatus.OK)
