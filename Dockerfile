FROM python:3.10-slim AS base

WORKDIR /usr/src

COPY . .

RUN apt-get -q update && apt-get -qy install netcat lsof curl
RUN curl -o /usr/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && chmod +x /usr/bin/wait-for
RUN pip install poetry
RUN poetry config virtualenvs.create false

# ======== Development ======== #

FROM base AS development

ENV PYTHONPATH=/fastapi_test

RUN poetry install --no-root

# ======== Production ======== #

# Pull base image
FROM base AS production

ENV PYTHONPATH=/fastapi_test

RUN poetry install --no-root --no-dev

EXPOSE 8000

CMD ["poetry", "run", "start"]
