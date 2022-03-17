import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def app():
    from fastapi_test.app import app

    return app


@pytest.fixture()
def api_client(app):
    return TestClient(app)
