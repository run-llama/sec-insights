# https://hub.docker.com/_/python
FROM python:3.11.3-slim-bullseye

ENV PYTHONUNBUFFERED True
# Install other backend deps
RUN apt-get update
RUN apt-get install libpq-dev gcc build-essential wkhtmltopdf s3fs -y
RUN pip install poetry==1.6.1
# Install frontend node modules
ENV APP_HOME /app
COPY . $APP_HOME

CMD ["/bin/bash"]
