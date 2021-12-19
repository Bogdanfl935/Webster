from app.constants import endpoint_constants, storage_constants
from app.utilities import url_joiner, api_utilities
import requests


def make_next_url_post(authenticated_user):
    target_url = url_joiner.urljoin(endpoint_constants.STORAGE_MS_URL, endpoint_constants.NEXT_URL)
    response = requests.get(target_url, json=dict(
        username=authenticated_user, quantity=storage_constants.CRAWLER_URL_QUANTITY))
    return api_utilities.unpack_response(response)


def make_pending_url_delete(authenticated_user, page_url):
    # TODO
    pass
