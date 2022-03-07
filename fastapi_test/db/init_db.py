import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from .base import Base


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "")
    db = os.getenv("POSTGRES_DB", "fastapi")
    return f"postgresql://{user}:{password}@{server}/{db}"


engine = create_engine(get_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init() -> None:
    # Create database if it does not exist.
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        # Connect the database if exists.
        engine.connect()

    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    pass
