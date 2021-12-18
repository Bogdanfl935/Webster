from http import HTTPStatus

from app.config.redis_config import redis_memory_usage
from flask import request, Response


def set_memory_usage():
    username = request.json.get("username", None)
    memory_usage = request.json.get("memoryUsage", None)

    redis_memory_usage.incr(username, memory_usage)

    return Response(status=HTTPStatus.OK)


def get_memory_usage():
    username = request.args.get("username")
    result = redis_memory_usage.get(username)
    if result is not None:
        result = str(result.decode('utf-8'))

    return {"username": username, "memoryUsage": result}
