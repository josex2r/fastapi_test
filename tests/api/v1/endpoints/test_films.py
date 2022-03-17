from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from fastapi_test.api.deps import get_films_crud
from fastapi_test.models.film import Film

subject = Film(
    id=1,
    title="A New Hope",
    description="A long time ago in a galaxy far, far away...",
    year=1977,
    rating=4,
)


class AsyncMagicMock(MagicMock):
    data: Any

    def __await__(self, *args, **kwargs):
        self.__call__(*args, **kwargs)  # track calls using "assert_called_with"
        yield from []  # this function must return an iterator, force yield
        return self.data


@pytest.fixture
def mock_films_crud(app) -> MagicMock:
    films_crud = MagicMock()
    films_crud.get_multi.return_value = AsyncMagicMock()
    films_crud.get_by_title.return_value = AsyncMagicMock()
    films_crud.create.return_value = AsyncMagicMock()
    films_crud.update.return_value = AsyncMagicMock()
    films_crud.get.return_value = AsyncMagicMock()
    films_crud.remove.return_value = AsyncMagicMock()
    return films_crud


@pytest.fixture
def override_films_crud_dep(app, mock_films_crud, autouse=True) -> None:
    # https://github.com/tiangolo/fastapi/issues/3331
    app.dependency_overrides[get_films_crud] = lambda: mock_films_crud


async def test_get_films(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.get_multi.return_value.data = [subject]

    response = api_client.get("/v1/films")

    assert response.status_code == 200
    assert response.json() == [subject.as_dict()]


@pytest.mark.parametrize(
    "params, result",
    [
        (None, {"skip": 0, "limit": 100}),
        ({"skip": 1, "limit": 2}, {"skip": 1, "limit": 2}),
    ],
)
async def test_get_films_params(
    api_client: TestClient, mock_films_crud, override_films_crud_dep, params, result
) -> None:
    mock_films_crud.get_multi.return_value.data = [subject]

    api_client.get("/v1/films", params=params)

    mock_films_crud.get_multi.assert_called_with(**result)


async def test_get_film(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.get_by_title.return_value.data = subject

    response = api_client.get("/v1/films/foo")

    assert response.status_code == 200
    assert response.json() == subject.as_dict()


async def test_get_film_ko(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.get_by_title.return_value.data = None

    response = api_client.get("/v1/films/foo")

    assert response.status_code == 404
    assert response.json() == {"detail": "Film not found"}


async def test_create_film(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.create.return_value.data = subject

    response = api_client.post("/v1/films/", json=subject.as_dict())

    assert response.status_code == 201
    assert response.json() == subject.as_dict()


async def test_update_film(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.get.return_value.data = subject
    mock_films_crud.update.return_value.data = subject

    response = api_client.put("/v1/films/1", json=subject.as_dict())

    assert response.status_code == 200
    assert response.json() == subject.as_dict()


async def test_update_film_ko(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.get.return_value.data = None

    response = api_client.put("/v1/films/1", json=subject.as_dict())

    assert response.status_code == 404
    assert response.json() == {"detail": "Film not found"}


async def test_delete_film(
    api_client: TestClient, mock_films_crud, override_films_crud_dep
) -> None:
    mock_films_crud.remove.return_value.data = subject

    response = api_client.delete("/v1/films/1")

    assert response.status_code == 200
    assert response.json() == subject.as_dict()
