from app.constants import serialization_constants, sql_models
from app.services import persistence_service
from app.services.user_mapping_service import fetch_user_id
from flask import request, Response, make_response, jsonify
from http import HTTPStatus
import base64


def add_image():
    user_id = fetch_user_id(request.json.get(serialization_constants.USERNAME_KEY))
    extension = request.json.get(serialization_constants.EXTENSION_KEY)
    content = base64.b64decode(request.json.get(serialization_constants.CONTENT_KEY).encode('ascii'))
    record = sql_models.ParsedImage(user_id=user_id, extension=extension, content=content)

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

    query_func = lambda session: session.query(sql_models.ParsedImage).filter(
        sql_models.ParsedImage.user_id == user_id).values(
        sql_models.ParsedImage.id, sql_models.ParsedImage.extension, sql_models.ParsedImage.content)
    records = persistence_service.query(query_func)
    response = {serialization_constants.PARSED_IMAGES_KEY: [
            {key: base64.b64encode(value).decode("ascii") if key == serialization_constants.CONTENT_KEY else value 
            for key, value in record._asdict().items()}
        for record in records]
    }
    return make_response(jsonify(response), HTTPStatus.OK)
