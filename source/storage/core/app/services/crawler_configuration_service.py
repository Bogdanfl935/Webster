from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.user_mapping_service import fetch_user_id
from flask import request, make_response, jsonify, Response, abort
from http import HTTPStatus

def get_configuration_options():
    # User ID is not used as configuration options are not distinguished between users
    # If different options are introduced for users, the User ID may
    # be used to fetch associated configuration options (i.e. according to their account
    # status perks)
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    query_func = lambda session: session.query(sql_models.CrawlerOption).values(
        sql_models.CrawlerOption.keyword, sql_models.CrawlerOption.description)
    records = persistence_service.query(query_func)
    response = {serialization_constants.OPTIONS_KEY: [record._asdict() for record in records]}

    return make_response(jsonify(response), HTTPStatus.OK)

def get_configuration():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    query_func = lambda session: session.query(sql_models.CrawlerOption).join(
        sql_models.CrawlerConfiguration).filter(sql_models.CrawlerConfiguration.user_id == user_id,
        sql_models.CrawlerConfiguration.option_id == sql_models.CrawlerOption.id).values(
        sql_models.CrawlerOption.keyword)
    records = persistence_service.query(query_func)
    response = {serialization_constants.OPTIONS_KEY: [record._asdict() for record in records]}

    return make_response(jsonify(response), HTTPStatus.OK)

def set_configuration():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    keyword = request.json.get(serialization_constants.KEYWORD_KEY)
    active = request.json.get(serialization_constants.ACTIVE_KEY)

    fetch_query_func = lambda session: session.query(sql_models.CrawlerOption).filter(
        sql_models.CrawlerOption.keyword == keyword).one_or_none()
    option_record = persistence_service.query(fetch_query_func)

    if option_record is None:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY)

    if active is True:
        record = sql_models.CrawlerConfiguration(user_id=user_id, option_id=option_record.id)
        persistence_service.add(record)
    else:
        query_func = lambda session: session.query(sql_models.CrawlerConfiguration).filter(
            sql_models.CrawlerConfiguration.user_id == user_id, 
            sql_models.CrawlerConfiguration.option_id == option_record.id).delete()
        persistence_service.query(query_func)

    persistence_service.commit_session()
    return Response(status=HTTPStatus.OK)