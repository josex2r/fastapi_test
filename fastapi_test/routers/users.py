import aiohttp
from fastapi import APIRouter, HTTPException, status

from ..models.user import User
from ..utils.arequest import arequest

router = APIRouter(tags=["users"])


@router.get("/", response_model=list[User])
async def get_users() -> list[User]:
    async with arequest[list[User]](
        "https://jsonplaceholder.typicode.com/users"
    ) as result:
        response, data = result
        return data


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    async with arequest[User](
        f"https://jsonplaceholder.typicode.com/users/{user_id}"
    ) as result:
        response, data = result
        return data


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: User,
) -> User:
    async with arequest[User](
        "https://jsonplaceholder.typicode.com/users", method="post", json=user.to_json()
    ) as result:
        response, data = result
        if response.status != status.HTTP_201_CREATED:
            raise HTTPException(
                status_code=response.status, detail="Error creating user"
            )
        return data
