import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def api_client():
    from fastapi_test.app import app

    return TestClient(app)
