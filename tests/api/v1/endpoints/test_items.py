from fastapi.testclient import TestClient
from fastapi_test.models.item import Item

import pytest


@pytest.fixture()
def api_client():
    from fastapi_test.app import app

    return TestClient(app)


def test_read_item(api_client):
    response = api_client.get("/v1/items/1")

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 1,
    }


def test_create_item(api_client):
    item = Item(name="foo", description="bar", price=5, tax=0.1)
    response = api_client.post("/v1/items", json=item.dict())

    assert response.status_code == 200
    assert response.json() == {
        **item.dict(),
        "price_with_tax": 5.1
    }


def test_update_item(api_client):
    item = Item(name="foo", description="bar", price=5, tax=0.1)
    response = api_client.put("/v1/items/1", json=item.dict())

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 1,
        **item.dict(),
    }
