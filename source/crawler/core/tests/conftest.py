import pytest
# from app import main

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app import main

@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    client = main.app.test_client()
    yield client
