Check env var:
export POETRY_VIRTUALENVS_CREATE=true

Create codespace from 

# Shell # 1 - Configure services

* setup .env
cd backend
poetry shell
poetry install
set -a
source .env
# This compose up will report an error on first run
docker compose up
* take down docker compose up
make migrate # bootstraps the database by starting it in docker compose and running alambric
make run

# Shell # 2 - Populate database

cd backend
poetry shell
poetry intall
set -a
source .env
make seed_db_local

# Shell # 3 - Run Web app

# configure .env with local path to web server

cd frontend
set -a
source .env
npm install
npm

# Shell # 4 - Interactive shell

cd backend
poetry shell
make chat
create
detail
message Hi





Add Postres Host Access Trust:

db:
    image: ankane/pgvector:v0.5.0
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: llama_app_db
      POSTGRES_HOST_AUTH_METHOD: trust
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data/




* Ensure the .env file has been updated to include your OPENAI_API_KEY *

Terminal commands:

### First Terminal - Setup the Servers

```sh
cd backend
poetry shell
poetry install
set -a
source .env
docker compose up
```

* This will error on first run *
Shut down docker compose, on mac [Ctrl + C]

```sh
make migrate
make run
```

### Second Terminal - Populate Database

With the first terminal still running proceed in a new one with:

```sh
cd backend
poetry shell
poetry intall
set -a
source .env
make seed_db_local
```

### Third Terminal - Front End

```sh
cd frontend
cp .env.example .env
set -a
source .env
npm install
npm run dev
```

Open browser to "http://127.0.0.1:3000/"

### Fourth Terminal - Interactive Query

```sh
cd backend
poetry shell
make chat
```

You should see a prompt indicator like: (Chat🦙)

```sh
(Chat🦙) create
(Chat🦙) detail
(Chat🦙) message Hi
```