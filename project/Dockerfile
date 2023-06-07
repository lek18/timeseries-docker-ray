# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /src/app

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

# run the script and save output to both inside the container and host volume
ENTRYPOINT ["python", "-u", "app/main.py"]
