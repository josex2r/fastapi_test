from typing import Optional

from pydantic import BaseModel


class FilmBase(BaseModel):
    title: str
    description: Optional[str] = None
    year: int
    rating: int


class FilmCreate(FilmBase):
    description: str


# Properties to receive on item update
class FilmUpdate(FilmBase):
    pass


class FilmInDBBase(FilmBase):
    id: int

    class Config:
        orm_mode = True


class Film(FilmInDBBase):
    pass


class FilmInDB(FilmInDBBase):
    pass
