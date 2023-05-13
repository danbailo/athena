FROM python:3.11.3-slim-buster

RUN apt-get update && apt-get install \
        --no-install-recommends -qq -y \
    build-essential \
    gcc \
    g++ \
    libpoppler-cpp-dev \
    poppler-utils \
    pkg-config \
    libpq-dev

WORKDIR /project

COPY ./pylintrc /project/pylintrc

COPY ./requirements.txt /project/requirements.txt
COPY ./requirements-dev.txt /project/requirements-dev.txt

RUN pip install --upgrade pip
RUN pip install -r /project/requirements.txt -r /project/requirements-dev.txt

COPY ./alembic.ini /project/alembic.ini
COPY ./alembic /project/alembic

COPY ./src /project/

RUN rm requirements.txt requirements-dev.txt