from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..db.init_db import get_db
from ..crud.film import crud
from ..models.film import Film
from ..schemas import film as film_schema

router = APIRouter(tags=["films"])


@router.get("/", response_model=list[film_schema.Film])
def get_films(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[Film]:
    """
    Retrieve films.
    """
    films = crud.get_multi(db, skip=skip, limit=limit)
    return films


@router.get("/{film_name}", response_model=film_schema.Film)
def get_film_by_title(
    film_name: str,
    db: Session = Depends(get_db),
) -> Optional[Film]:
    """
    Retrieve a film by title.
    """
    film = crud.get_by_title(db, film_name)
    return film


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=film_schema.Film)
def create_film(
    film_in: film_schema.FilmCreate,
    db: Session = Depends(get_db)
) -> Film:
    """
    Create a film.
    """
    film = crud.create(db, obj_in=film_in)
    return film


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=film_schema.Film)
def update_film(
    id: int,
    film_in: film_schema.FilmUpdate,
    db: Session = Depends(get_db)
) -> Film:
    """
    Update a film.
    """
    film = crud.get(db=db, id=id)
    if not film:
        raise HTTPException(status_code=404, detail="film not found")
    film = crud.update(db, obj_in=film_in, db_obj=film)
    return film


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=film_schema.Film)
def delete_film(
    id: int,
    film_in: film_schema.FilmUpdate,
    db: Session = Depends(get_db)
) -> Film:
    """
    Delete a film.
    """
    film = crud.get(db=db, id=id)
    if not film:
        raise HTTPException(status_code=404, detail="film not found")
    film = crud.remove(db, id=id)
    return film
