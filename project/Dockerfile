# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
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

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
