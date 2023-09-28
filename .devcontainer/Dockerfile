# https://hub.docker.com/_/python
FROM python:3.11.3-slim-bullseye

ENV PYTHONUNBUFFERED True
# Install Node.js 18.x
RUN apt-get update
RUN apt-get install -y ca-certificates curl gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update
RUN apt-get install nodejs -y
# Install docker
# Add Docker's official GPG key:
RUN apt-get update
RUN apt-get install ca-certificates curl gnupg
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg

# Add the docker repository to Apt sources:
RUN  echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
# Install AWS CLI
RUN apt-get install unzip -y
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
# Install other backend deps
RUN apt-get install libpq-dev gcc build-essential wkhtmltopdf s3fs -y
RUN pip install poetry
# Install frontend node modules
ENV APP_HOME /app
COPY . $APP_HOME
WORKDIR $APP_HOME/frontend
RUN npm install
# Setup backend
WORKDIR $APP_HOME/backend
RUN poetry install

CMD ["/bin/bash"]
