from flask import request, Response, render_template
from app.constants import endpoint_constants, template_constants, serialization_constants
from app.utilities.url_joiner import construct_parameterized_url, urljoin
from app.utilities.api_utilities import unpack_response
import requests, json

def make_crawler_configuration_get(authenticated_user: str) -> dict:
    target_url = urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.CRAWLER_CONFIGURATION)
    parameterized_url = construct_parameterized_url(target_url, {serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_crawler_options_get(authenticated_user: str) -> dict:
    target_url = urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.CRAWLER_CONFIGURATION_OPTION)
    parameterized_url = construct_parameterized_url(target_url, {serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_parser_configuration_get(authenticated_user: str) -> dict:
    target_url = urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.PARSER_CONFIGURATION)
    parameterized_url = construct_parameterized_url(target_url, {serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_parser_configuration_post(response_object: Response, authenticated_user: str) -> dict:
    target_url = urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.PARSER_CONFIGURATION)
    response = requests.post(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.TAG_KEY: request.form.get(serialization_constants.TAG_KEY)
        })
    response_object.set_data(json.dumps(unpack_response(response)).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object

def make_parser_configuration_delete(response_object: Response, authenticated_user: str) -> dict:
    target_url = urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.PARSER_CONFIGURATION)
    response = requests.delete(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.TAG_KEY: request.form.get(serialization_constants.TAG_KEY)
        })
    response_object.set_data(json.dumps(unpack_response(response)).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object

def make_crawler_configuration_put(response_object: Response, authenticated_user: str) -> dict:
    target_url = urljoin(endpoint_constants.CONFIG_MS_URL, endpoint_constants.CRAWLER_CONFIGURATION)
    response = requests.put(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.KEYWORD_KEY: request.form.get(serialization_constants.KEYWORD_KEY),
        serialization_constants.ACTIVE_KEY: request.form.get(serialization_constants.ACTIVE_KEY)
        })
    response_object.set_data(json.dumps(unpack_response(response)).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object

def render_configuration(response_object: Response, authenticated_user: str) -> Response:
    parser_configuration_response, _ = make_parser_configuration_get(authenticated_user)
    crawler_configuration_options_response, _ = make_crawler_options_get(authenticated_user)
    crawler_configuration_response, _ = make_crawler_configuration_get(authenticated_user)
    parser_configuration_tags = parser_configuration_response.get(serialization_constants.TAGS_KEY)
    crawler_configuration_possible_options = crawler_configuration_options_response.get(serialization_constants.OPTIONS_KEY)
    crawler_configuration_selected_options = crawler_configuration_response.get(serialization_constants.OPTIONS_KEY)
    # keyword, description
    selected_options_set = set(
        (option_dict.get(serialization_constants.KEYWORD_KEY) for option_dict in crawler_configuration_selected_options))

    response_object.set_data(
        render_template(
            template_constants.SECTION_CONFIGURATION_PATH,
            authenticated_user=authenticated_user,
            crawler_config=[
                option_dict | {serialization_constants.ACTIVE_KEY: True 
                    if option_dict.get(serialization_constants.KEYWORD_KEY) in selected_options_set else False} 
                for option_dict in crawler_configuration_possible_options],
            parser_config = parser_configuration_tags
        )
    )
    return response_object

