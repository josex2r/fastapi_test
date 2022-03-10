from fastapi import APIRouter, HTTPException, status

from fastapi_test.models.people import Person
from fastapi_test.utils.arequest import arequest

router = APIRouter()


@router.get("/", response_model=list[Person])
async def get_people() -> list[Person]:
    async with arequest[list[Person]](
        "https://jsonplaceholder.typicode.com/users"
    ) as result:
        response, data = result
        return data


@router.get("/{person_id}", response_model=Person)
async def get_person(person_id: int) -> Person:
    async with arequest[Person](
        f"https://jsonplaceholder.typicode.com/users/{person_id}"
    ) as result:
        response, data = result
        return data


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Person)
async def create_person(
    person: Person,
) -> Person:
    async with arequest[Person](
        "https://jsonplaceholder.typicode.com/users", method="post", json=person.to_json()
    ) as result:
        response, data = result
        if response.status != status.HTTP_201_CREATED:
            raise HTTPException(
                status_code=response.status, detail="Error creating person"
            )
        return data
