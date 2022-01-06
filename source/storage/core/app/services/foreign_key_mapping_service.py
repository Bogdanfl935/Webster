from app.services import persistence_service
from app.constants.sql_models import User, ParsedUrl
from flask import abort
from http import HTTPStatus

def fetch_user_id(authenticated_user: str):
    query_func = lambda session: session.query(User).filter(User.username == authenticated_user).value(User.id)
    user_id = persistence_service.query(query_func)
    if user_id is None:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY)
    return user_id

def fetch_source_id(user_id: int, source: str):
    query_func = lambda session: session.query(ParsedUrl).filter(
        ParsedUrl.user_id == user_id, ParsedUrl.url == source).value(ParsedUrl.id)
    source_id = persistence_service.query(query_func)
    if source_id is None:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY)
    return source_id
