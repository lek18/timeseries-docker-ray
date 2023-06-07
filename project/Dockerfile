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

# add app
COPY . .

# create a directory for host volume
RUN mkdir -p /host-data

# set file permissions for the host volume directory
RUN chown -R root:root /host-data

# run the script and save output to both inside the container and host volume
CMD ["python", "-u", "app/main.py", "/src/app/data/predictions.csv", "/host-data/predictions.csv"]
