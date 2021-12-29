from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.user_mapping_service import fetch_user_id
from flask import request, Response, make_response, jsonify
from http import HTTPStatus



def get_tags():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    query_func = lambda session: session.query(sql_models.ParserConfiguration).filter(
        sql_models.ParserConfiguration.user_id == user_id).values(sql_models.ParserConfiguration.tag)
    records = persistence_service.query(query_func)
    response = {serialization_constants.TAGS_KEY: [record._asdict() for record in records]}
    return make_response(jsonify(response), HTTPStatus.OK)

def add_tag():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    tag = request.json.get(serialization_constants.TAG_KEY)
    record = sql_models.ParserConfiguration(user_id=user_id, tag=tag)
    persistence_service.add(record, commit=True)
    return Response(status=HTTPStatus.OK)

def delete_tag():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    tag = request.json.get(serialization_constants.TAG_KEY)
    query_func = lambda session: session.query(sql_models.ParserConfiguration).filter(
        sql_models.ParserConfiguration.user_id == user_id,
        sql_models.ParserConfiguration.tag == tag).one_or_none()
    record = persistence_service.query(query_func)

    if record is not None:
        persistence_service.delete(record, commit=True)

    return Response(status=HTTPStatus.OK)