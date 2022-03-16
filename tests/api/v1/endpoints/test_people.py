from typing import Type

import pytest
from pytest_mock import MockerFixture

from fastapi_test.models.people import Address, Company, LatLng, Person

from ....conftest import AsyncContextManagerMock

subject = Person(
    id=1,
    name="foo",
    username="bar",
    email="foo@foo.com",
    phone="1234567890",
    website="https://foo.com",
    address=Address(
        street="123 Main St",
        suite="Apt 123",
        city="Foo",
        zipcode="12345",
        geo=LatLng(lat="123", lng="456"),
    ),
    company=Company(
        name="Foo Inc",
        catchPhrase="Foo",
        bs="Foo",
    ),
)


@pytest.fixture()
def mock_arequest(mocker: MockerFixture) -> Type[AsyncContextManagerMock]:
    arequest_mock = mocker.patch("fastapi_test.api.v1.endpoints.people.arequest")
    arequest_mock.__getitem__.return_value = AsyncContextManagerMock

    return arequest_mock.__getitem__.return_value


def test_get_people(api_client, mock_arequest):
    mock_arequest.data = [subject.dict()]

    response = api_client.get("/v1/people")

    assert response.status_code == 200
    assert response.json() == [subject]


def test_get_person(api_client, mock_arequest):
    mock_arequest.data = subject.dict()

    response = api_client.get("/v1/people/1")

    assert response.status_code == 200
    assert response.json() == subject


def test_create_person_ok(api_client, mock_arequest):
    mock_arequest.data = subject.dict()
    mock_arequest.response.status = 201

    response = api_client.post("/v1/people/", json=mock_arequest.data)

    assert response.status_code == 201
    assert response.json() == subject


def test_create_person_ko(api_client, mock_arequest):
    mock_arequest.data = subject.dict()
    mock_arequest.response.status = 500

    response = api_client.post("/v1/people/", json=mock_arequest.data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Error creating person"}
