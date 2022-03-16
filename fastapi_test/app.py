from fastapi import FastAPI, Request

from fastapi_test.api.v1.api import api_router
from fastapi_test.db.init_db import init
from fastapi_test.utils import cat_fact

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init()


app.include_router(api_router, prefix="/v1")


@app.get("/")
def root(request: Request) -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/cat-fact")
async def get_cat_fact() -> cat_fact.CatFact:
    return await cat_fact.get_cat_fact()
