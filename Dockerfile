# ======== Development ======== #

FROM python:3.10 AS development

RUN apt-get -q update && apt-get -qy install netcat lsof
RUN curl -o /usr/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && chmod +x /usr/bin/wait-for

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

RUN wait-for postgres_fastapi:5432

ENV PYTHONPATH=/fastapi_test

WORKDIR /usr/src

# ======== Production ======== #

# Pull base image
FROM python:3.10 AS production

WORKDIR /usr/src

# Install dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . .
RUN poetry install --no-dev

ENV PYTHONPATH=/fastapi_test

EXPOSE 8000

CMD ["poetry", "run", "start"]
