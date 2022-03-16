from typing import Optional
from unittest.mock import MagicMock, Mock

import pytest
from aiohttp import ClientResponse, web


@pytest.fixture
def app():
    app = web.Application()
    return app


@pytest.fixture
def cli(app, loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def arequest_session(cli):
    from fastapi_test.utils.arequest import arequest

    arequest_instance = arequest("/")
    arequest_instance.session = cli

    return arequest_instance


class AsyncContextManagerMock(MagicMock):
    data: dict = {}
    response: Mock = Mock()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __aenter__(self) -> tuple[Optional[ClientResponse], dict]:
        return self.response, self.data

    async def __aexit__(self, *args) -> None:
        pass
