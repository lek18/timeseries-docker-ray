# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1\
    POETRY_VERSION=1.4.1


# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc curl\
  && apt-get clean

# install poetry - respects $POETRY_VERSION & $POETRY_HOME

RUN pip install --upgrade pip\
    pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false

# install python dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

# add app
COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh"]
