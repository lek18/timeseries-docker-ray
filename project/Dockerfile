# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
RUN mkdir -p /src

# create the app user
# RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV APP_HOME=/src
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.1

# install poetry
RUN pip install --upgrade pip && pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false

# install python dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

# add app
COPY . .
