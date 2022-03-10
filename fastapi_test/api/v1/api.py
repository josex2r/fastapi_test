from fastapi import APIRouter

from .endpoints import films, items, people, users

api_router = APIRouter()

api_router.include_router(
    router=films.router,
    prefix="/films",
    tags=["router"],
)

api_router.include_router(
    router=items.router,
    prefix="/items",
    tags=["router"],
)

api_router.include_router(
    router=people.router,
    prefix="/people",
    tags=["router"],
)

api_router.include_router(
    router=users.router,
    prefix="/users",
    tags=["router"],
)
