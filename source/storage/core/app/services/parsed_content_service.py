from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.user_mapping_service import fetch_user_id
from flask import request, Response, make_response, jsonify
from http import HTTPStatus
import base64


def add_content():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    tag = request.json.get(serialization_constants.TAG_KEY)
    content = base64.b64decode(request.json.get(serialization_constants.CONTENT_KEY).encode('ascii'))
    record = sql_models.ParsedContent(user_id=user_id, tag=tag, content=content)

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
    query_func = lambda session: session.query(sql_models.ParsedContent).filter(
        sql_models.ParsedContent.user_id == user_id).values(
        sql_models.ParsedContent.id, sql_models.ParsedContent.tag, sql_models.ParsedContent.content)
    records = persistence_service.query(query_func)
    response = {serialization_constants.PARSED_CONTENT_KEY: [
            {key: base64.b64encode(value).decode("utf-8") if key == serialization_constants.CONTENT_KEY else value 
            for key, value in record._asdict().items()}
        for record in records]
    }
    return make_response(jsonify(response), HTTPStatus.OK)
