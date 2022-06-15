FROM python:3.8

RUN mkdir -p /srv/app

WORKDIR /srv/app

COPY . .

RUN pip install poetry
RUN poetry install

WORKDIR /srv/app/server

EXPOSE 8050
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8050
