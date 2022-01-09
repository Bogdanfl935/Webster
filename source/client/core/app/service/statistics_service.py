from app.constants import endpoint_constants, serialization_constants
from app.utilities.api_utilities import unpack_response
from app.utilities.url_joiner import urljoin, construct_parameterized_url
from flask import Response, jsonify
import json, requests

def make_statistics_public_chart_get():
    target_url = urljoin(endpoint_constants.STATISTICS_MS_URL, endpoint_constants.STATISTICS_PUBLIC_CHART)
    response, status = unpack_response(requests.get(target_url))
    return jsonify(response), status

def make_statistics_public_get():
    target_url = urljoin(endpoint_constants.STATISTICS_MS_URL, endpoint_constants.STATISTICS_PUBLIC)
    response, status = unpack_response(requests.get(target_url))
    return jsonify(response), status

def make_statistics_private_chart_get(response_object: Response, authenticated_user: str):
    target_url = urljoin(endpoint_constants.STATISTICS_MS_URL, endpoint_constants.STATISTICS_PRIVATE_CHART)
    parameterized_url = construct_parameterized_url(target_url, {serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    response_object.set_data(json.dumps(unpack_response(response)).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object

def make_statistics_private_get(response_object: Response, authenticated_user: str):
    target_url = urljoin(endpoint_constants.STATISTICS_MS_URL, endpoint_constants.STATISTICS_PRIVATE)
    parameterized_url = construct_parameterized_url(target_url, {serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    response_object.set_data(json.dumps(unpack_response(response)).encode('utf-8'))
    response_object.mimetype = 'application/json'
    return response_object