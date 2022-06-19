FROM python:3.8

RUN mkdir -p /srv/app

WORKDIR /srv/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8888
ENTRYPOINT python run.py
