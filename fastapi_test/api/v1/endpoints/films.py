from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException

from fastapi_test.crud.film import CRUDFilm
from fastapi_test.models.film import Film
from fastapi_test.schemas import film as film_schema
from fastapi_test.api.deps import get_films_crud

router = APIRouter()


@router.get("/", response_model=list[film_schema.Film])
async def get_films(
    skip: int = 0,
    limit: int = 100,
    crud: CRUDFilm = Depends(get_films_crud),
) -> list[Film]:
    """
    Retrieve films.
    """
    films = await crud.get_multi(skip=skip, limit=limit)
    return films


@router.get("/{film_name}", response_model=film_schema.Film)
async def get_film_by_title(
    film_name: str,
    crud: CRUDFilm = Depends(get_films_crud),
) -> Optional[Film]:
    """
    Retrieve a film by title.
    """
    film = await crud.get_by_title(film_name)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return film


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=film_schema.Film)
async def create_film(
    film_in: film_schema.FilmCreate,
    crud: CRUDFilm = Depends(get_films_crud),
) -> Film:
    """
    Create a film.
    """
    film = await crud.create(obj_in=film_in)
    return film


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=film_schema.Film)
async def update_film(
    id: int,
    film_in: film_schema.FilmUpdate,
    crud: CRUDFilm = Depends(get_films_crud),
) -> Film:
    """
    Update a film.
    """
    film = await crud.get(id=id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    film = await crud.update(obj_in=film_in, db_obj=film)
    return film


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=film_schema.Film)
async def delete_film(
    id: int,
    crud: CRUDFilm = Depends(get_films_crud),
) -> Optional[Film]:
    """
    Delete a film.
    """
    film = await crud.remove(id=id)
    return film
