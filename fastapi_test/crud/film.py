from typing import Optional
from sqlalchemy.orm import Session

from ..models.film import Film
from ..schemas.film import FilmCreate, FilmUpdate
from .base import CRUDBase


class CRUDItem(CRUDBase[Film, FilmCreate, FilmUpdate]):
    def get_by_title(self, db: Session, title: str) -> Optional[Film]:
        return db.query(self.model).filter(self.model.title == title).first()


crud = CRUDItem(Film)
