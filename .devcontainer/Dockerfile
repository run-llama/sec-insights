# https://hub.docker.com/_/python
# FROM python:3.11.3-slim-bullseye
FROM python:3.11.7-slim-bookworm

# 3.11.3
ENV PYTHON_VERSION 3.11.7
# 3.11.3
ENV PYENV_VERSION=3.11.7
# 1.6.1
ENV POETRY_VERSION=1.7.1
ENV PYTHONUNBUFFERED True

# Install other backend deps
RUN apt-get update
RUN apt-get install -y --no-install-recommends wkhtmltopdf s3fs libpq-dev gcc make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
RUN apt-get install -y mecab-ipadic-utf8

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration: (plus POETRY_VERSION)
  POETRY_NO_INTERACTION=1 \
  # POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'



# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
# WORKDIR ${HOME}/backend

# COPY poetry.lock pyproject.toml /backend/
RUN poetry config virtualenvs.create false


# Set the working directory to /app
WORKDIR /workspaces/sec-insights/backend

# Copy the poetry files into the container at /app
# COPY backend/pyproject.toml backend/poetry.lock /app/
COPY backend/pyproject.toml /workspaces/sec-insights/backend/

# Install project dependencies
RUN poetry install

# Copy the entire project into the container at /app
# COPY backend /app/

# RUN poetry install --no-dev
# cache
# COPY poetry.lock pyproject.toml /backend/

# RUN pip install poetry==${POETRY_VERSION}
# ENV HOME="/root"

# WORKDIR ${HOME}
# RUN apt-get install -y git
# RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv

# ENV PYENV_ROOT="${HOME}/.pyenv"
# ENV PATH="$PYENV_ROOT/shims:${PYENV_ROOT}/bin:${PATH}"
# RUN pyenv install 3.11.3 \
#     && pyenv global 3.11.3 \
#     && pyenv rehash

# Install pyenv
# RUN ls -la /root/.pyenv
# RUN cat /root/.pyenv

# RUN set -ex \
#     && curl https://pyenv.run | bash
# RUN pyenv update \
#     && pyenv install $PYTHON_VERSION \
#     && pyenv global $PYTHON_VERSION \
#     && pyenv rehash

# Install frontend node modules
# ENV APP_HOME /app
# COPY . ${APP_HOME}

# RUN cd backend && poetry && poetry install

# CMD ["/bin/bash"]
CMD ["poetry"]