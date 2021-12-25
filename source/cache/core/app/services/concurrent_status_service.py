from http import HTTPStatus
from app.constants import serialization_constants
from app.services.concurrent_access_service import acquire_lock, release_lock
from app.constants.lock_types import LockType
from app.config.redis_config import redis_crawler_status, redis_parser_status
from flask import request, make_response, jsonify, Response
from redis import Redis

def get_crawler_active_status():
    return _get_active_status(redis_crawler_status)

def get_parser_active_status():
    return _get_active_status(redis_parser_status)

def get_and_set_crawler_active_status():
    return _get_and_set_active_status(redis_crawler_status, LockType.CRAWLER_STATUS_LOCK)

def get_and_set_parser_active_status():
    return _get_and_set_active_status(redis_parser_status, LockType.PARSER_STATUS_LOCK)

def set_crawler_active_status():
    return _set_active_status(redis_crawler_status, LockType.CRAWLER_STATUS_LOCK)

def set_parser_active_status():
    return _set_active_status(redis_parser_status, LockType.PARSER_STATUS_LOCK)


def _set_active_status(redis_database: Redis, lock: LockType):
    username = request.json.get(serialization_constants.USERNAME_KEY)
    active = request.json.get(serialization_constants.STATUS_KEY)

    if active is False: # Avoid caching if not neccessary => Remove entry if no longer active
        acquire_lock(lock) # Enter critical section
        redis_database.delete(username)
        release_lock(lock) # Exit critical section
    
    return Response(status=HTTPStatus.OK)

def _get_and_set_active_status(redis_database: Redis, lock: LockType):
    username = request.json.get(serialization_constants.USERNAME_KEY)
    
    acquire_lock(lock) # Enter critical section
    active = bool(redis_database.get(username).decode('utf-8')) if redis_database.exists(username) != 0 else False
    if active is False: # Read and set active to True in an atomic operation
        redis_database.set(username, bytes(True))
    release_lock(lock) # Exit critical section

    return make_response(jsonify(dict(active=active)), HTTPStatus.OK)

def _get_active_status(redis_database: Redis):
    username = request.args.get(serialization_constants.USERNAME_KEY)
    active = bool(redis_database.get(username).decode('utf-8')) if redis_database.exists(username) != 0 else False
    return make_response(jsonify(dict(active=active)), HTTPStatus.OK)
