from http import HTTPStatus

from app.config.redis_config import redis_status
from flask import request, Response


def get_active_status():
    username = request.args.get("username")
    result = redis_status.get(username)
    if result:
        result = bool(result.decode('utf-8'))

    return {"active": result}


def set_active_status():
    username = request.json.get("username", None)
    active = request.json.get("active", None)

    redis_status.set(username, active)
    return Response(status=HTTPStatus.OK)
