cd backend/

# install poetry dependencies
poetry install

cp .env.development .env
set -a
source .env
make migrate
