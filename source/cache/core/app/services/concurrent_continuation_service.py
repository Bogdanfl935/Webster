from http import HTTPStatus
from app.constants import serialization_constants
from app.services.concurrent_access_service import acquire_lock, release_lock
from app.constants.lock_types import LockType
from app.config.redis_config import redis_crawler_continuation, redis_parser_continuation
from flask import request, make_response, jsonify, Response
from redis import Redis


def get_and_set_crawler_continuation_status():
    return _get_and_set_continuation_status(redis_crawler_continuation, LockType.CRAWLER_CONTINUATION_LOCK)

def get_and_set_parser_continuation_status():
    return _get_and_set_continuation_status(redis_parser_continuation, LockType.PARSER_CONTINUATION_LOCK)

def set_crawler_continuation_status():
    return _set_continuation_status(redis_crawler_continuation, LockType.CRAWLER_CONTINUATION_LOCK)

def set_parser_continuation_status():
    return _set_continuation_status(redis_parser_continuation, LockType.PARSER_CONTINUATION_LOCK)

def _get_and_set_continuation_status(redis_database: Redis, lock: LockType):
    username = request.json.get(serialization_constants.USERNAME_KEY)
    
    acquire_lock(lock) # Enter critical section
    continuation = bool(redis_database.get(username).decode('utf-8')) if redis_database.exists(username) != 0 else True
    if continuation is False: # Read and clear continuation in an atomic operation
        redis_database.delete(username)
    release_lock(lock) # Exit critical section

    return make_response(jsonify(dict(continuation=continuation)), HTTPStatus.OK)


def _set_continuation_status(redis_database: Redis, lock: LockType):
    username = request.json.get(serialization_constants.USERNAME_KEY)
    continuation = request.json.get(serialization_constants.CONTINUATION_KEY)

    if continuation is False: # Avoid caching if not neccessary => Only cache if continuation is false
        acquire_lock(lock) # Enter critical section
        redis_database.set(username, bytes(continuation))
        release_lock(lock) # Exit critical section

    return Response(status=HTTPStatus.OK)
