FROM python:3.8

RUN mkdir -p /srv/app

WORKDIR /srv/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9000
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 9000
