from pydantic.dataclasses import dataclass


@dataclass
class Film:
    title: str
    year: int
    rating: int

    def __init__(self, title: str, year: int, rating: int):
        self.title = title
        self.year = year
        self.rating = rating

    def __str__(self):
        stars = "☆" * self.rating
        return f"{self.title} ({self.year}) - {stars}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.title == other.title and self.year == other.year and self
