# https://hub.docker.com/_/python
FROM python:3.11.3-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME/frontend
RUN npm install
WORKDIR $APP_HOME/backend
RUN pip install poetry
COPY . ./
RUN apt-get update
RUN apt-get install libpq-dev gcc build-essential wkhtmltopdf  -y
# Add Docker's official GPG key:
RUN apt-get update
RUN apt-get install ca-certificates curl gnupg
RUN  install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg

# Add the docker repository to Apt sources:
RUN  echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
RUN poetry install

# Run python process that just runs the code snippet "import app"
RUN cp .env.example .env
RUN set -a && source .env
RUN make migrate
# import app.main to run PGVector table creation
RUN poetry run python -c "import app.main"

CMD ["/bin/bash"]
