from typing import Generic, TypeVar

import aiohttp

ResponseType = TypeVar("ResponseType")


class arequest(Generic[ResponseType]):
    def __init__(self, url: str, *, method: str = "get", **rest):
        self.url = url
        self.rest = rest
        self.method = method
        self.session = aiohttp.ClientSession()

    async def __aenter__(self) -> tuple[aiohttp.ClientResponse, ResponseType]:
        # func = getattr(self.session, self.method)
        # self.response = await func(self.url, **self.rest)
        self.response = await self.session.request(self.method, self.url, **self.rest)
        data = await self.response.json()
        return self.response, data

    async def __aexit__(self, *args):
        self.response.close()
        await self.session.close()
