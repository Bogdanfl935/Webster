def test_in_post_link(client):
    request_payload = {"startLink": "https://mihai-2-tw.logitrex.ro/"}
    response = client.post("/crawler", json=request_payload)
    result = response.get_json()

    assert response.status_code == 200
    assert result is not None
    print(result)
    assert "ana" in result
    assert result['ana'] == "mere"


def test_in_get_data(client):
    response = client.get('/crawler')
    result = response.get_json()
    assert result is not None

    assert response.status_code == 200
    assert result is not None
    assert "ala" in result
    assert result['ala'] == "bala"