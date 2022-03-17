# fastapi_test

This is just a test project to learn [fastAPI](https://fastapi.tiangolo.com/) + `python` an more the related things.

> Directories & ORM inspired in [](ttps://github.com/tiangolo/full-stack-fastapi-postgresql)

## Tools

- [Poetry](https://python-poetry.org/)
- [fastAPI](https://fastapi.tiangolo.com/)
- [pydantic](https://pydantic-docs.helpmanual.io/)
- [sqlAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/) + [compose](https://docs.docker.com/compose/)
- [pytest](https://docs.pytest.org/en/7.1.x/)

## Run

```bash
# development
docker-compose up development
# app ready in http://localhost:8000

# production (@TODO)
docker-compose up production
# app ready in http://localhost:80
```

## Test

```bash
pytest --cov=fastapi_test --cov-report=html -s tests
```
