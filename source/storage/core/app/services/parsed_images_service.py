from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.foreign_key_mapping_service import fetch_user_id, fetch_source_id
from flask import request, Response, make_response, jsonify
from http import HTTPStatus
import base64


def add_image():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    source_id = fetch_source_id(user_id, request.json.get(serialization_constants.SOURCE_KEY))
    extension = request.json.get(serialization_constants.EXTENSION_KEY)
    content = base64.b64decode(request.json.get(serialization_constants.CONTENT_KEY).encode('ascii'))
    record = sql_models.ParsedImage(user_id=user_id, extension=extension, content=content, source_id=source_id)

    persistence_service.add(record, commit=True)
    return Response(status=HTTPStatus.OK)

def delete_image():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    content_id = request.json.get(serialization_constants.ID_KEY)
    query_func = lambda session: session.query(sql_models.ParsedImage).filter(
        sql_models.ParsedImage.user_id == user_id,
        sql_models.ParsedImage.id == content_id).delete()
    
    persistence_service.query(query_func)
    persistence_service.commit_session()

    return Response(status=HTTPStatus.OK)

def get_images():
    user_id = fetch_user_id(request.args.get(serialization_constants.USERNAME_KEY))
    source = request.args.get(serialization_constants.SOURCE_KEY, None)

    if source is not None:
        source_id = fetch_source_id(user_id, source)
        auxiliary_condition = sql_models.ParsedImage.source_id == source_id
    else:
        auxiliary_condition = True

    query_func = lambda session: session.query(sql_models.ParsedImage).join(sql_models.ParsedUrl).filter(
        sql_models.ParsedImage.user_id == user_id, auxiliary_condition).values(
        sql_models.ParsedImage.id, sql_models.ParsedImage.extension, 
        sql_models.ParsedImage.content, sql_models.ParsedUrl.url.label(serialization_constants.SOURCE_KEY))
    records = persistence_service.query(query_func)
    response = {serialization_constants.PARSED_IMAGES_KEY: [
            {key: base64.b64encode(value).decode("utf-8") if key == serialization_constants.CONTENT_KEY else value 
            for key, value in record._asdict().items()}
        for record in records]
    }
    return make_response(jsonify(response), HTTPStatus.OK)
