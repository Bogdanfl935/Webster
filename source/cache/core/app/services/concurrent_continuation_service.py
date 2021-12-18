from http import HTTPStatus

from app.config.redis_config import redis_continuation
from flask import request, Response


def get_continuation_status():
    username = request.json.get("username", None)
    result = redis_continuation.get(username)
    if result is not None:
        result = bool(result.decode('utf-8'))

    return {"continuation": result}


def set_continuation_status():
    username = request.json.get("username", None)
    continuation = request.json.get("continuation", None)

    redis_continuation.set(username, continuation)

    return Response(status=HTTPStatus.OK)
