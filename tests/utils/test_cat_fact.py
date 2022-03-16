from typing import Type

import pytest
from pytest_mock import MockerFixture

from ..conftest import AsyncContextManagerMock


@pytest.fixture()
def mock_arequest(mocker: MockerFixture) -> Type[AsyncContextManagerMock]:
    arequest_mock = mocker.patch("fastapi_test.utils.cat_fact.arequest")
    arequest_mock.__getitem__.return_value = AsyncContextManagerMock

    return arequest_mock.__getitem__.return_value


async def test_return_types(mock_arequest) -> None:
    from fastapi_test.utils.cat_fact import CatFact, get_cat_fact

    mock_arequest.data = {"fact": "cat fact", "length": "3"}

    result = await get_cat_fact()

    assert isinstance(result, CatFact)
    assert isinstance(result.length, int)
    assert isinstance(result.fact, str)


async def test_returns_request_data(mock_arequest) -> None:
    from fastapi_test.utils.cat_fact import get_cat_fact

    mock_arequest.data = {"fact": "cat fact", "length": "3"}

    result = await get_cat_fact()

    assert result == {"fact": "cat fact", "length": 3}
