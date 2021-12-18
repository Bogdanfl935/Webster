from http import HTTPStatus

from app.config.redis_config import redis_last_url
from flask import request, Response


def get_last_url():
    username = request.args.get("username")
    result = redis_last_url.get(username)
    if result is not None:
        result = str(result.decode('utf-8'))

    return {"username": username, "lastUrl": result}


def set_last_url():
    username = request.json.get("username", None)
    last_url = request.json.get("lastUrl", None)

    redis_last_url.set(username, last_url)

    return Response(status=HTTPStatus.OK)
