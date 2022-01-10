from app.utilities import url_joiner
from app.utilities.api_utilities import unpack_response
from app.constants import endpoint_constants, serialization_constants
import requests

def make_export_content_get(authenticated_user: str, source: str):
    target_url = url_joiner.urljoin(endpoint_constants.EXPORTER_MS_URL, endpoint_constants.EXPORT_CONTENT)
    parameterized_url = url_joiner.construct_parameterized_url(
        target_url, parameters={
            serialization_constants.USERNAME_KEY: authenticated_user,
            serialization_constants.SOURCE_KEY: source
    })
    response = requests.get(parameterized_url)
    return unpack_response(response, check_content_length=False)