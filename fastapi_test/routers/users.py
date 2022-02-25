import aiohttp
from fastapi import APIRouter, status

from ..models.user import User
from ..utils.arequest import arequest

router = APIRouter(tags=["users"])


@router.get("/")
async def get_users() -> list[User]:
    async with arequest("https://jsonplaceholder.typicode.com/users") as response:
        users = await response.json()
        return [*map(lambda data: User(**data), users)]


@router.get("/{user_id}")
async def get_user(user_id: int) -> User:
    async with arequest(f"https://jsonplaceholder.typicode.com/users/{user_id}") as resp:
        user = await resp.json()
        return User(**user)


@router.post("/")
async def create_user(user: User, status_code=status.HTTP_201_CREATED) -> User:
    async with arequest("https://jsonplaceholder.typicode.com/users", method="post", json=user.to_json()) as resp:
        if resp.status != status.HTTP_201_CREATED:
            raise Exception(f"Error creating user: {resp.status}")
        user = await resp.json()
        return User(**user)
