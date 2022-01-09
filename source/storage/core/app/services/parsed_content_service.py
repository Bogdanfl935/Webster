from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.foreign_key_mapping_service import fetch_user_id, fetch_source_id
from flask import request, Response, make_response, jsonify
from http import HTTPStatus
import base64


def add_content():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    source_id = fetch_source_id(user_id, request.json.get(serialization_constants.SOURCE_KEY))
    tag = request.json.get(serialization_constants.TAG_KEY)
    content = base64.b64decode(request.json.get(serialization_constants.CONTENT_KEY).encode('ascii'))
    record = sql_models.ParsedContent(user_id=user_id, tag=tag, content=content, source_id=source_id)

    persistence_service.add(record, commit=True)
    return Response(status=HTTPStatus.OK)

def delete_content():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    content_id = request.json.get(serialization_constants.ID_KEY)
    query_func = lambda session: session.query(sql_models.ParsedContent).filter(
        sql_models.ParsedContent.user_id == user_id,
        sql_models.ParsedContent.id == content_id).delete()
    
    persistence_service.query(query_func)
    persistence_service.commit_session()

    return Response(status=HTTPStatus.OK)

def get_content():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    source = request.args.get(serialization_constants.SOURCE_KEY, None)

    if source is not None:
        source_id = fetch_source_id(user_id, source)
        auxiliary_condition = sql_models.ParsedContent.source_id == source_id
    else:
        auxiliary_condition = True

    query_func = lambda session: session.query(sql_models.ParsedContent).join(sql_models.ParsedUrl).filter(
        sql_models.ParsedContent.user_id == user_id, auxiliary_condition).values(
        sql_models.ParsedContent.id, sql_models.ParsedContent.tag,
        sql_models.ParsedContent.content, sql_models.ParsedUrl.url.label(serialization_constants.SOURCE_KEY))
    records = persistence_service.query(query_func)
    response = {serialization_constants.PARSED_CONTENT_KEY: [
            {key: base64.b64encode(value).decode("utf-8") if key == serialization_constants.CONTENT_KEY else value 
            for key, value in record._asdict().items()}
        for record in records]
    }
    return make_response(jsonify(response), HTTPStatus.OK)

def get_content_source():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    parsed_content_query_func = lambda session: session.query(sql_models.ParsedContent).join(
        sql_models.ParsedUrl).filter(sql_models.ParsedContent.user_id == user_id).values(
            sql_models.ParsedContent.id,
            sql_models.ParsedUrl.url.label(serialization_constants.SOURCE_KEY))
    parsed_content_records = persistence_service.query(parsed_content_query_func)
    parsed_content_sources = {serialization_constants.SOURCES_KEY: [record[1] for record in parsed_content_records]}

    parsed_image_query_func = lambda session: session.query(sql_models.ParsedImage).join(
        sql_models.ParsedUrl).filter(sql_models.ParsedImage.user_id == user_id).values(
            sql_models.ParsedContent.id,
            sql_models.ParsedUrl.url.label(serialization_constants.SOURCE_KEY))
    parsed_image_records = persistence_service.query(parsed_image_query_func)
    parsed_image_sources = {serialization_constants.SOURCES_KEY: [record[1] for record in parsed_image_records]}

    response = {serialization_constants.SOURCES_KEY: list(set(
        parsed_content_sources.get(serialization_constants.SOURCES_KEY) + \
            parsed_image_sources.get(serialization_constants.SOURCES_KEY)))}
    return make_response(jsonify(response), HTTPStatus.OK)
