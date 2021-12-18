import pytest
from app import main


@pytest.fixture
def client():
    main.flask_app.config['TESTING'] = True
    client = main.flask_app.test_client()
    yield client
