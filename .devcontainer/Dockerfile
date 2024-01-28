# https://hub.docker.com/_/python
FROM python:3.11.3-slim-bullseye

ENV PYTHON_VERSION 3.11.3
ENV PYTHONUNBUFFERED True
# Install other backend deps
RUN apt-get update
RUN apt-get install -y --no-install-recommends wkhtmltopdf s3fs libpq-dev gcc make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
RUN apt-get install -y mecab-ipadic-utf8
RUN pip install poetry==1.6.1

ENV HOME="/root"

WORKDIR $HOME
RUN apt-get install -y git
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv

ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN pyenv install 3.11.3
RUN pyenv global 3.11.3

# Install pyenv
RUN set -ex \
    && curl https://pyenv.run | bash \
    && pyenv update \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && pyenv rehash

# Install frontend node modules
ENV APP_HOME /app
COPY . $APP_HOME

CMD ["/bin/bash"]
