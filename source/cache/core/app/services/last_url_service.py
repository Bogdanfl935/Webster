import json

from app.config.redis_config import redis_last_url


def get_last_url(username):
    result = redis_last_url.get(username)
    if result:
        result = str(result.decode('utf-8'))
    else:
        result = None

    return json.dumps({"username": username, "lastUrl": result})


def set_last_url(username, last_url):
    redis_last_url.set(username, last_url)
