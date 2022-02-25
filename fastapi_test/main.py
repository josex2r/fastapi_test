from typing import Any

import uvicorn
from fastapi import FastAPI, Request

from .routers.films import router as films_router
from .routers.items import router as items_router
from .routers.users import router as users_router
from .utils import cat_fact

app = FastAPI()

app.include_router(
    router=films_router,
    prefix="/films",
    tags=["router"],
)

app.include_router(
    router=items_router,
    prefix="/items",
    tags=["router"],
)

app.include_router(
    router=users_router,
    prefix="/users",
    tags=["router"],
)


@app.get("/")
def root(request: Request) -> dict[str, str]:
    print(request.url)
    return {"message": "Hello World"}


@app.get("/cat-fact")
async def get_cat_fact() -> cat_fact.CatFact:
    return await cat_fact.get_cat_fact()


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
