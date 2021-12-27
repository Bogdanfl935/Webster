from http import HTTPStatus
from app.constants import serialization_constants
from app.services.concurrent_access_service import acquire_lock, release_lock
from app.constants.lock_types import LockType
from app.config.redis_config import redis_crawler_continuation
from flask import request, make_response, jsonify, Response


def get_and_set_crawler_continuation_status():
    username = request.json.get(serialization_constants.USERNAME_KEY)

    acquire_lock(LockType.CRAWLER_CONTINUATION_LOCK)  # Enter critical section
    continuation = bool(redis_crawler_continuation.get(username).decode(
        'utf-8')) if redis_crawler_continuation.exists(username) != 0 else True
    if continuation is False:  # Read and clear continuation in an atomic operation
        redis_crawler_continuation.delete(username)
    release_lock(LockType.CRAWLER_CONTINUATION_LOCK)  # Exit critical section

    return make_response(jsonify(dict(continuation=continuation)), HTTPStatus.OK)


def set_crawler_continuation_status():
    username = request.json.get(serialization_constants.USERNAME_KEY)
    continuation = request.json.get(serialization_constants.CONTINUATION_KEY)

    if continuation is False: # Avoid caching if not neccessary => Only cache if continuation is false
        acquire_lock(LockType.CRAWLER_CONTINUATION_LOCK) # Enter critical section
        redis_crawler_continuation.set(username, bytes(continuation))
        release_lock(LockType.CRAWLER_CONTINUATION_LOCK) # Exit critical section

    return Response(status=HTTPStatus.OK)
