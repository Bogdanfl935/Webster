import constants
import endpoint_constants

def test_handle_config_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.CONFIGURATION, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None
    assert "specific-tag" in result
    assert "same-page" in result
    assert "storage-limit" in result
