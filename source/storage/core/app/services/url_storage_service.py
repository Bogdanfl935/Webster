from app.constants import serialization_constants, sql_models
from app.services import persistence_service, concurrent_access_service
from app.services.user_mapping_service import fetch_user_id
from flask import request, make_response, jsonify, Response
from http import HTTPStatus



def add_bulk_urls():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    urls = request.json.get(serialization_constants.URLS_KEY)

    concurrent_access_service.acquire_user_lock(user_id)
    try:
        for url in urls:
            persistence_service.add(sql_models.ParsedUrl(user_id=user_id, url=url, state=sql_models.UrlState.READY))
            persistence_service.commit_session(supress_exceptions=True)
    finally:
        concurrent_access_service.release_user_lock(user_id)

    return Response(status=HTTPStatus.OK)
    

def fetch_next_urls():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    quantity = request.json.get(serialization_constants.QUANTITY_KEY)
    fetch_query_func = lambda session: session.query(sql_models.ParsedUrl).filter(
        sql_models.ParsedUrl.state == sql_models.UrlState.READY).limit(quantity)

    concurrent_access_service.acquire_user_lock(user_id)
    try:
        records = persistence_service.query(fetch_query_func)
        response = {serialization_constants.URLS_KEY: [record.url for record in records]}
        update_query_func = lambda session: session.query(sql_models.ParsedUrl).filter(
            sql_models.ParsedUrl.id.in_([record.id for record in records])).update(
                {sql_models.ParsedUrl.state: sql_models.UrlState.PENDING})
        persistence_service.query(update_query_func)
        persistence_service.commit_session()
    finally:
        concurrent_access_service.release_user_lock(user_id)
    return make_response(jsonify(response), HTTPStatus.OK)

def update_bulk_pending_url_states():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    urls = request.json.get(serialization_constants.URLS_KEY)
    visited = request.json.get(serialization_constants.VISITED_KEY)

    state = sql_models.UrlState.VISITED if visited is True else sql_models.UrlState.READY
    update_query_func = lambda session: session.query(sql_models.ParsedUrl).filter(
        sql_models.ParsedUrl.user_id == user_id, sql_models.ParsedUrl.url.in_(urls),
        sql_models.ParsedUrl.state == sql_models.UrlState.PENDING).update({sql_models.ParsedUrl.state: state})

    concurrent_access_service.acquire_user_lock(user_id)
    try:
        persistence_service.query(update_query_func)
        persistence_service.commit_session()
    finally:
        concurrent_access_service.release_user_lock(user_id)
    
    return Response(status=HTTPStatus.OK)