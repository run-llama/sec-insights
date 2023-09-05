# https://hub.docker.com/_/python
FROM python:3.11.3-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
RUN pip install poetry
COPY . ./
RUN apt-get update
RUN apt-get install libpq-dev gcc build-essential wkhtmltopdf  -y
RUN poetry install

ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

CMD ["poetry", "run", "start"]
