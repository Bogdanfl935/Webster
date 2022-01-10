from app.constants import serialization_constants, template_constants
from flask import Response, render_template, request
from app.service import storage_service, export_service
import json

def render_archive(response_object: Response, authenticated_user: str):
    response, status = storage_service.make_content_source_get(authenticated_user)
    response_object.set_data(
        render_template(
            template_constants.SECTION_ARCHIVE_PATH,
            authenticated_user=authenticated_user,
            content_sources=response.get(serialization_constants.SOURCES_KEY)
        )
    )
    return response_object, status

def make_export_content_get(response_object: Response, authenticated_user: str):
    source = request.json.get(serialization_constants.SOURCE_KEY)
    response, status = export_service.make_export_content_get(authenticated_user, source)
    response_object.set_data(json.dumps(response).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object, status

def make_content_source_delete(response_object: Response, authenticated_user: str):
    source = request.json.get(serialization_constants.SOURCE_KEY)
    response, status =  storage_service.make_content_source_delete(authenticated_user, source)
    response_object.set_data(json.dumps(response).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object, status