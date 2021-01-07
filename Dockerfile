FROM python:3.8.6-slim-buster

COPY ["pyproject.toml", "poetry.lock", "./"]

RUN apt-get update && \
    apt-get install -y git gcc neofetch && \
    python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi 

COPY . .

WORKDIR /

RUN touch /configuration.yml

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]