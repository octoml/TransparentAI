FROM python:3.8

ENV \
  # Keeps Python from generating .pyc files in the container
  PYTHONDONTWRITEBYTECODE=1 \
  # Turns off buffering for easier container logging
  PYTHONUNBUFFERED=1 \
  # Install a handler to dump traceback    
  PYTHONFAULTHANDLER=1

# Install and setup poetry
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl netcat \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir -p /srv/app
WORKDIR /srv/app
COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

CMD python run.py
EXPOSE 8888
