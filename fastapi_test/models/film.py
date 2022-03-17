from sqlalchemy import Column, Integer, String

from ..db.base import Base


class Film(Base):
    title = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    year = Column(Integer)
    rating = Column(Integer)

    def __str__(self):
        stars = "☆" * self.rating
        return f"{self.title} ({self.year}) - {stars}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        print(self)
        print(other)
        return self.title == other.title and self.year == other.year and self
