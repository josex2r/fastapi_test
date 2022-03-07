from typing import AsyncGenerator

from ..db.init_db import async_session
from ..crud.film import CRUDFilm
from ..models.film import Film


async def get_films_crud() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield CRUDFilm(Film, session)
