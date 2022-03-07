from typing import TypedDict

from pydantic import BaseModel

from .arequest import arequest


class CatFactDict(TypedDict):
    fact: str
    length: int


class CatFact(BaseModel):
    fact: str
    length: int


async def get_cat_fact() -> CatFact:
    async with arequest[CatFactDict]("https://catfact.ninja/fact") as result:
        response, data = result
        return CatFact(**data)
