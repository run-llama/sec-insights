run:
	echo "Running in local mode."
	docker compose start db
	docker compose start localstack
	poetry run start

run_docker:
	echo "Running in local mode with docker."
	# Check if .env file would set the DATABASE_URL parameter and ask the user to remove it
	# from .env if it would
	# This is needed because the DATABASE_URL parameter is set in docker-compose.yml
	# Also account for the case where DATABASE_URL exists but has been commented out by
	# doing a regex match to see that its at the start of a line
	if [ -f .env ] && grep -q -E '^\s*DATABASE_URL\s*=' .env; then \
		echo "The .env file contains a DATABASE_URL parameter. Please remove it from the .env file and try again."; \
		exit 1; \
	fi
	docker compose up

migrate:
	echo "Running migrations."
	docker compose start db
	poetry run python -m alembic upgrade head

test:
	poetry run python -m pytest tests/

chat:
	poetry run python -m scripts.chat_llama

setup_localstack:
	docker compose start localstack
	echo "Waiting for localstack to start..."
	sleep 3
	awslocal s3 mb s3://${S3_ASSET_BUCKET_NAME}
	awslocal s3 cp /tmp/index.html s3://${S3_ASSET_BUCKET_NAME}/index.html
	rm /tmp/index.html
	awslocal s3 website s3://${S3_ASSET_BUCKET_NAME}/ --index-document index.html
	awslocal s3api put-bucket-cors --bucket ${S3_ASSET_BUCKET_NAME} --cors-configuration file://./localstack-cors-config.json

seed_db_based_on_env:
	# Call either seed_db or seed_db_preview, seed_db_local based on the environment
	# This is used by the CI/CD pipeline
	ENVIRONMENT=$$(poetry run python -c "from app.core.config import settings;print(settings.ENVIRONMENT.value)"); \
	echo "Environment: $$ENVIRONMENT"; \
	if [ "$$ENVIRONMENT" = "preview" ]; then \
		make seed_db_preview; \
	elif [ "$$ENVIRONMENT" = "production" ]; then \
		make seed_db; \
	else \
		make seed_db_local; \
	fi

seed_db:
	echo "Seeding database."
	poetry run python scripts/seed_db.py

seed_db_preview:
	echo "Seeding database for Preview."
	# only need to populate with two companies for Preview
	poetry run python scripts/seed_db.py  --ciks '["0001018724", "1326801"]'

seed_db_local:
	echo "Seeding database for local."
	echo "<html>Hello world</html>" > /tmp/index.html
	docker compose start db
	make setup_localstack
	python scripts/seed_db.py --ciks '["0001018724", "1326801"]'  --filing_types '["10-K"]'
