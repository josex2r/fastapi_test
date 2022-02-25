import aiohttp
from pydantic import BaseModel


class CatFact(BaseModel):
    fact: str
    length: int


async def get_cat_fact() -> CatFact:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://catfact.ninja/fact') as response:
            data = await response.json()
            return CatFact(**data)
