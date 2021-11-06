import json

import endpoint_constants
import constants

def test_in_get_data(client):
    response = client.post(endpoint_constants.STORAGE)
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None
    assert "ala" in result
    assert result['ala'] == "bala"


def test_in_get_next_links(client):
    send_data = {"quantity": constants.NEXT_LINK_LIMIT}
    response = client.post(endpoint_constants.NEXT_LINK, data = json.dumps(send_data))
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None
    assert "urls" in result
    assert result['urls'] == ["https://apple.com/", "https://www.google.com/", "https://www.youtube.com/"]


