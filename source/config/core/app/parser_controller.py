from app.constants import endpoint_constants
from app.validation import validation_schema
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import parser_configuration_service
from flask import Blueprint, Response

parser = Blueprint('parser', __name__)

@parser.route(endpoint_constants.PARSER_CONFIGURATION, methods=['POST'])
@validate_with_schema(validation_schema.ParserConfigurationSchema)
def handle_parser_configuration_post() -> Response:
    return parser_configuration_service.add_tag()

@parser.route(endpoint_constants.PARSER_CONFIGURATION, methods=['DELETE'])
@validate_with_schema(validation_schema.ParserConfigurationSchema)
def handle_parser_configuration_delete() -> Response:
    return parser_configuration_service.delete_tag()


@parser.route(endpoint_constants.PARSER_CONFIGURATION, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_parser_configuration_get() -> Response:
    return parser_configuration_service.get_tags()