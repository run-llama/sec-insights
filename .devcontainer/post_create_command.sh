cd backend/

pip install --upgrade pip
# install poetry dependencies
poetry install

cp .env.development .env
set -a
source .env
make migrate
