from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import content_caching_service
from app.validation import validation_schema
from app.constants import endpoint_constants
from flask import Blueprint, Response

parser = Blueprint('parser', __name__)


@parser.route(endpoint_constants.LAST_PARSED, methods=['POST'])
@validate_with_schema(validation_schema.LastParsedSchema)
def handle_last_parsed_post() -> Response:
    return content_caching_service.set_last_parsed()


@parser.route(endpoint_constants.LAST_PARSED, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_last_parsed_get() -> Response:
    return content_caching_service.get_last_parsed()