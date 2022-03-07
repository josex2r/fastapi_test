from typing import Optional
from sqlalchemy.future import select

from ..models.film import Film
from ..schemas.film import FilmCreate, FilmUpdate
from .base import CRUDBase


class CRUDFilm(CRUDBase[Film, FilmCreate, FilmUpdate]):
    async def get_by_title(self, title: str) -> Optional[Film]:
        sentence = select(self.model).where(self.model.title == title)
        query = await self.session.execute(sentence)
        return query.scalars().first()
