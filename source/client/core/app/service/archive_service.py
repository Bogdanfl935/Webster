from app.constants import serialization_constants, template_constants
from flask import Response, render_template
from app.service import storage_service
import requests, json

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
    return storage_service.make_export_content_get(authenticated_user)

def make_parsed_content_delete(response_object: Response, authenticated_user: str):
    pass

def make_parsed_image_delete(response_object: Response, authenticated_user: str):
    pass