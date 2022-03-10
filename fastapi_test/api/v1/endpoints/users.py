from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_test.api.deps import get_current_user, get_users_crud
from fastapi_test.models.user import User
from fastapi_test.crud.user import CRUDUser

router = APIRouter()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_crud: CRUDUser = Depends(get_users_crud)
):
    user = await users_crud.get_by_username_and_password(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": user.id,
        "token_type": "bearer"
    }
