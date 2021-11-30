from app.constants import endpoint_constants


def test_handle_config_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.CONFIGURATION, json=request_payload)
    result = response.get_json(force=True)

    assert response.status_code == 200
    assert result is not None

def test_handle_config_retr_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.RETRIEVE_CONFIGURATION_CONFIG, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None