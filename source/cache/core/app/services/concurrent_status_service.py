import json

from app.config.redis_config import redis_status


def get_active_status(username):
    result = redis_status.get(username)
    if result:
        result = str(result.decode('utf-8'))
    else:
        result = None

    return json.dumps({"active": result})


def set_active_status(username, active):
    redis_status.set(username, active)
