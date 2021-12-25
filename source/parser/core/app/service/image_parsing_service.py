from app.constants import parsing_constants
from app.service import url_parsing_service, executor_service, generic_parsing_service, cache_service
from urllib.parse import urlparse, urlunparse
from mimetypes import guess_extension
import base64, requests, logging, traceback
from bs4.element import ResultSet

def process_images(authenticated_user: str, content_iterable: ResultSet, memory_limit, referrer: str):
    image_sources = (source for image in content_iterable if (source := image.get('src')) is not None)
    executor_service.acquire_user_lock(authenticated_user) # Enter critical section

    tag_content_binaries = generic_parsing_service.extract_content(
        authenticated_user = authenticated_user, 
        fetched_content = image_sources,
        memory_limit = memory_limit, 
        binary_conversion_func = lambda source: _process_image_by_source(source, referrer)
    )

    if len(tag_content_binaries) > 0: # At least one tag had been successfully processed
        cache_service.make_memory_usage_post(sum(map(len, tag_content_binaries)))

    executor_service.release_user_lock(authenticated_user) # Exit critical section
    
    # TODO Save image_binaries (extension, binary) to parsed_images table

def _process_image_by_source(source, referrer):
    image_binary = None
    if parsing_constants.BASE_64_INDICATOR in source:
        image_binary = _base64_to_binary(source)
    else:
        # Append scheme and netloc to image sources if needed
        image_url_href = url_parsing_service._prepend_anchor_url_content(urlparse(source), referrer)
        image_binary = _href_to_binary(urlunparse(image_url_href))
    return image_binary
    

def _base64_to_binary(source: str):
    image_type, base64_encoding = source.split(parsing_constants.BASE_64_INDICATOR)
    extension = guess_extension(image_type[len(parsing_constants.BASE_64_DATA_PREFIX):])
    return extension, base64.decodebytes(base64_encoding.encode("ascii"))

def _href_to_binary(source: str):
    response = requests.get(source, stream = True)
    extension = guess_extension(response.headers['content-type'])
    return extension, response.content