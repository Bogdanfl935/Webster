from app.constants import endpoint_constants
from app.validation import validation_schema
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.services import parser_configuration_service, parsed_content_service, parsed_images_service
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


@parser.route(endpoint_constants.PARSED_CONTENT, methods=['POST'])
@validate_with_schema(validation_schema.ParsedContentInsertionSchema)
def handle_parsed_content_post() -> Response:
    return parsed_content_service.add_content()

@parser.route(endpoint_constants.PARSED_CONTENT, methods=['DELETE'])
@validate_with_schema(validation_schema.ParsedDataDeletionSchema)
def handle_parsed_content_delete() -> Response:
    return parsed_content_service.delete_content()

@parser.route(endpoint_constants.PARSED_CONTENT, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_parsed_content_get() -> Response:
    return parsed_content_service.get_content()


@parser.route(endpoint_constants.PARSED_IMAGE, methods=['POST'])
@validate_with_schema(validation_schema.ParsedImageInsertionSchema)
def handle_parsed_image_post() -> Response:
    return parsed_images_service.add_image()

@parser.route(endpoint_constants.PARSED_IMAGE, methods=['DELETE'])
@validate_with_schema(validation_schema.ParsedDataDeletionSchema)
def handle_parsed_image_delete() -> Response:
    return parsed_images_service.delete_image()

@parser.route(endpoint_constants.PARSED_IMAGE, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_parsed_image_get() -> Response:
    return parsed_images_service.get_images()