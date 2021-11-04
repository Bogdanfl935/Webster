import constants
import endpoint_constants

def test_in_post_link(client):
    request_payload = {constants.START_LINK_KEY: constants.START_LINK_VAL}
    response = client.post(endpoint_constants.CRAWLER, json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None
    print(result)
    assert "error_code" in result
    assert result['error_code'] == 404


def test_in_get_data(client):
    response = client.get(endpoint_constants.CRAWLER)
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None
    assert "ala" in result
    assert result['ala'] == "bala"