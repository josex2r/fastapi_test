from typing import Optional

from sqlalchemy.future import select

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from .base import CRUDBase


def fake_hash_password(password: str):
    return "fakehashed-" + password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username_and_password(self, username: str, password: str) -> Optional[User]:
        hashed_password = fake_hash_password(password)
        sentence = select(self.model).where(
            self.model.username == username,
            self.model.hashed_password == hashed_password
        )
        query = await self.session.execute(sentence)
        return query.scalars().first()
