from http import HTTPStatus
from app.utilities import url_joiner, base64_encoder
from app.utilities.api_utilities import unpack_response
from app.service import executor_service
from app.constants import endpoint_constants, serialization_constants
import requests, itertools

def make_memory_limit_get(authenticated_user: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.MEMORY_LIMIT)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={serialization_constants.USERNAME_KEY: authenticated_user})
    response = requests.get(parameterized_url)
    return unpack_response(response)

def make_parsed_images_post(authenticated_user: str, tag_content_binaries: list, source: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.PARSED_IMAGE)
    json_serializable_content = list(itertools.starmap(
        lambda extension, content: (extension, base64_encoder.binary_to_base64_string(content)), tag_content_binaries))
    message, status = None, HTTPStatus.OK

    for (extension, content) in json_serializable_content:
        task = lambda: requests.post(target_url, json={
            serialization_constants.USERNAME_KEY: authenticated_user,
            serialization_constants.EXTENSION_KEY: extension,
            serialization_constants.CONTENT_KEY: content,
            serialization_constants.SOURCE_KEY: source})
        executor_service.submit_task(task)

    return message, status

def make_parsed_content_post(authenticated_user: str, tag_content_binaries: list, tag: str, source: str):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.PARSED_CONTENT)
    json_serializable_content = list(map(base64_encoder.binary_to_base64_string, tag_content_binaries))
    message, status = None, HTTPStatus.OK

    for content in json_serializable_content:
        task = lambda: requests.post(target_url, json={
            serialization_constants.USERNAME_KEY: authenticated_user,
            serialization_constants.TAG_KEY: tag,
            serialization_constants.CONTENT_KEY: content,
            serialization_constants.SOURCE_KEY: source})
        executor_service.submit_task(task)

    return message, status

def make_url_storage_post(authenticated_user: str, urls: list):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.URL_STORAGE)
    requests.post(target_url, json={
        serialization_constants.USERNAME_KEY: authenticated_user,
        serialization_constants.URLS_KEY: urls})
