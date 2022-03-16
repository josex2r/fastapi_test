from aiohttp import web, ClientResponse


async def fake_request(request):
    return web.Response(body='{"foo": "bar"}', content_type="application/json")


async def test_return_types(app, arequest_session) -> None:
    app.router._frozen = False
    app.router.add_get("/", fake_request)

    async with arequest_session as result:
        response, data = result

        assert isinstance(data, dict)
        assert isinstance(response, ClientResponse)


async def test_request_method(app, arequest_session) -> None:
    app.router._frozen = False
    app.router.add_post("/", fake_request)

    arequest_session.method = 'post'

    async with arequest_session as result:
        response, data = result

        assert data == {"foo": "bar"}
