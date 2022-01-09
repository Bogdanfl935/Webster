from http import HTTPStatus
from app.constants import serialization_constants
from app.services.concurrent_access_service import acquire_lock, release_lock
from app.services import storage_service
from app.constants.lock_types import LockType
from app.config.redis_config import redis_crawler_status, redis_memory_usage
from flask import request, make_response, jsonify, Response


def set_crawler_active_status():
    username = request.json.get(serialization_constants.USERNAME_KEY)
    active = request.json.get(serialization_constants.STATUS_KEY)

    if active is False:  # Avoid caching if not neccessary => Remove entry if no longer active
        acquire_lock(LockType.CRAWLER_STATUS_LOCK)  # Enter critical section
        try:
            if redis_memory_usage.exists(username) != 0:
                memory_usage = int(redis_memory_usage.get(username).decode('utf-8'))
                redis_memory_usage.delete(username)
                storage_service.make_memory_usage_put(username, memory_usage)
            redis_crawler_status.delete(username)
        finally:
            release_lock(LockType.CRAWLER_STATUS_LOCK)  # Exit critical section

    return Response(status=HTTPStatus.OK)


def get_and_set_crawler_active_status():
    username = request.json.get(serialization_constants.USERNAME_KEY)

    acquire_lock(LockType.CRAWLER_STATUS_LOCK)  # Enter critical section
    try:
        active = bool(redis_crawler_status.get(username).decode(
            'utf-8')) if redis_crawler_status.exists(username) != 0 else False
        if active is False:  # Read and set active to True in an atomic operation, update memory usage
            memory_usage_response, _ = storage_service.make_memory_usage_get(username)
            stored_memory_usage = memory_usage_response.get(serialization_constants.MEMORY_USAGE_KEY)
            cached_memory_usage = int(redis_memory_usage.get(username)) if redis_memory_usage.exists(username) != 0 else 0
            if stored_memory_usage > cached_memory_usage:
                redis_memory_usage.incr(username, stored_memory_usage)
            redis_crawler_status.set(username, bytes(True))
    finally:
        release_lock(LockType.CRAWLER_STATUS_LOCK)  # Exit critical section

    return make_response(jsonify(dict(active=active)), HTTPStatus.OK)


def get_crawler_active_status():
    username = request.args.get(serialization_constants.USERNAME_KEY)
    active = bool(redis_crawler_status.get(username).decode(
        'utf-8')) if redis_crawler_status.exists(username) != 0 else False
    return make_response(jsonify(dict(active=active)), HTTPStatus.OK)
