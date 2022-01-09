from flask import Blueprint, Response
from app.constants import  endpoint_constants
from app.services import crawler_configuration_service
from app.services.validation_service import validate_with_schema, ValidationTarget
from app.validation import validation_schema

crawler = Blueprint('crawler', __name__)

@crawler.route(endpoint_constants.CRAWLER_CONFIGURATION_OPTION, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_crawler_configuration_option_get() -> Response:
    return crawler_configuration_service.get_configuration_options()


@crawler.route(endpoint_constants.CRAWLER_CONFIGURATION, methods=['GET'])
@validate_with_schema(validation_schema.UsernameAccessSchema, target=ValidationTarget.NAMED_URL_PARAMETERS)
def handle_crawler_configuration_get() -> Response:
    return crawler_configuration_service.get_configuration()


@crawler.route(endpoint_constants.CRAWLER_CONFIGURATION, methods=['PUT'])
@validate_with_schema(validation_schema.CrawlerConfigurationSchema)
def handle_crawler_configuration_post() -> Response:
    return crawler_configuration_service.set_configuration()