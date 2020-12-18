FROM alpine:edge

COPY ["pyproject.toml", "poetry.lock", "./"]

ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0


RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk --no-cache add -q git mercurial cloc openssl openssl-dev openssh alpine-sdk bash gettext sudo build-base gnupg linux-headers xz \
    && apk add --no-cache python3 python3-dev py3-pip py3-wheel  py3-pillow py3-setuptools py3-numpy-dev py3-matplotlib py3-async-timeout  py3-psutil py3-beautifulsoup4 py3-cryptography poetry \
    && apk add --no-cache --virtual .build-deps gcc libffi libc-dev make zlib
RUN poetry config virtualenvs.create false && \
    pip install toml && \
    poetry install --no-dev --no-interaction --no-ansi && \
    apk del .build-deps



COPY . .

WORKDIR /

RUN touch /configuration.yml

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]