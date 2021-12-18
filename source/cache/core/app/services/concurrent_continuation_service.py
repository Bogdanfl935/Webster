import json

from app.config.redis_config import redis_continuation


def get_continuation_status(username):
    result = redis_continuation.get(username)
    if result:
        result = str(result.decode('utf-8'))
    else:
        result = None

    return json.dumps({"continuation": result})


def set_continuation_status(username, continuation):
    redis_continuation.set(username, continuation)
