from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapi_test.crud.film import CRUDFilm
from fastapi_test.crud.user import CRUDUser
from fastapi_test.db.init_db import async_session
from fastapi_test.models.film import Film
from fastapi_test.models.user import User


async def get_films_crud() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield CRUDFilm(Film, session)


async def get_users_crud() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield CRUDUser(User, session)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/users/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_crud: CRUDUser = Depends(get_users_crud)
):
    user_id = int(token)
    user = await users_crud.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user
