import endpoint_constants

def test_in_get_data(client):
    response = client.post(endpoint_constants.STORAGE)
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None
    assert "ala" in result
    assert result['ala'] == "bala"