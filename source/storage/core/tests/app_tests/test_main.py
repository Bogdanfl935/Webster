import json

import endpoint_constants
import constants

def test_handle_storage_post(client):
    response = client.post(endpoint_constants.STORAGE, json={"links": []})
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None


def test_handle_next_link_post(client):
    send_data = {"quantity": constants.NEXT_LINK_LIMIT}
    response = client.post(endpoint_constants.NEXT_LINK, data = json.dumps(send_data))
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None
    assert "urls" in result


