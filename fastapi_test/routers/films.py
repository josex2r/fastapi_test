from fastapi import APIRouter, status, Response

from ..models.film import Film

router = APIRouter(tags=["films"])

films: list[Film] = [
    Film("Star Wars", 1977, 5),
    Film("Lord of the Rings", 2001, 4),
]


@router.get("/")
def get_films() -> list[Film]:
    return films


@router.get("/{film_name}")
def get_film_by_title(film_name: str) -> Film:
    # return [film for film in films if film.title == film_name][0]
    return [*filter(lambda film: film.title == film_name, films)][0]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_film(film: Film) -> Film:
    films.append(film)
    return film


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_film(film: Film, response: Response) -> None:
    if film in films:
        films.remove(film)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
