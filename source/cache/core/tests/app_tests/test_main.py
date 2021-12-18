from app.constants import endpoint_constants


def test_handle_memory_usage_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.MEMORY_USAGE, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_memory_usage_get(client):
    response = client.get(endpoint_constants.MEMORY_USAGE)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_status_get(client):
    response = client.get(endpoint_constants.MEMORY_USAGE)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_concurrent_status_reading_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.MEMORY_USAGE, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_concurrent_status_writing_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.MEMORY_USAGE, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_concurrent_continuation_reading_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.MEMORY_USAGE, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_concurrent_continuation_writing_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.MEMORY_USAGE, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_last_url_post(client):
    request_payload = {}
    response = client.post(endpoint_constants.MEMORY_USAGE, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None


def test_handle_last_url_get(client):
    response = client.get(endpoint_constants.MEMORY_USAGE)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None
