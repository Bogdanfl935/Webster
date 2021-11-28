import constants
import endpoint_constants


def test_in_post_link(client):
  request_payload = constants.CONTENT_VAL
  response = client.post(endpoint_constants.PARSER, json=request_payload)
  result = response.get_json()

  assert response.status_code == 200
  assert result is not None
  assert "links" in result
