import pytest
from aiohttp import web, ClientResponse


async def fake_request(request):
    return web.Response(body='{"foo": "bar"}', content_type="application/json")


@pytest.fixture
def app():
    app = web.Application()
    app.router.add_get("/", fake_request)
    return app


@pytest.fixture
def cli(app, loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture()
def mock_arequest(cli):
    from fastapi_test.utils.arequest import arequest

    arequest_instance = arequest('/')
    arequest_instance.session = cli

    return arequest_instance


async def test_return_types(mock_arequest) -> None:
    async with mock_arequest as result:
        response, data = result

        assert isinstance(data, dict)
        assert isinstance(response, ClientResponse)


async def test_request_method(app, mock_arequest) -> None:
    app.router.add_post("/", fake_request)
    mock_arequest.method = 'post'

    async with mock_arequest as result:
        response, data = result

        assert data == {"foo": "bar"}
