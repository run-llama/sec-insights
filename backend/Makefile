run:
	echo "Running in local mode."
	docker compose create db localstack
	docker compose start db localstack
	poetry run start

run_docker:
	echo "Running in local mode with docker."
	docker compose up

migrate:
	echo "Running migrations."
	docker compose create db
	docker compose start db
	poetry run python -m alembic upgrade head
	# workaround for having PGVector create its tables
	poetry run python -m scripts.build_vector_tables

refresh_db:
	# First ask for confirmation.
	@echo -n "Are you sure you want to refresh the local database? This will delete all data in your local db. [Y/n] "; \
	read ans; \
	if [ $${ans:-'N'} = 'Y' ]; then make confirmed_refresh_db; else echo "Aborting."; fi

confirmed_refresh_db:
	echo "Refreshing database."
	docker compose down db
	docker volume rm backend_postgres_data
	make migrate

test:
	poetry run python -m pytest tests/

chat:
	poetry run python -m scripts.chat_llama

setup_localstack:
	docker compose create localstack
	docker compose start localstack
	echo "Waiting for localstack to start..."
	# Ping http://localhost:4566/health until we get a 200 response
	until $$(curl --output /dev/null --silent --head --fail http://localhost:4566/health); do \
		printf '.'; \
		sleep 0.5; \
	done
	# Check that S3_ASSET_BUCKET_NAME is set
	if [ -z ${S3_ASSET_BUCKET_NAME} ]; then \
		echo "S3_ASSET_BUCKET_NAME is not set. Please set it and try again."; \
		exit 1; \
	fi
	awslocal s3 mb s3://${S3_ASSET_BUCKET_NAME}
	echo "<html>LocalStack S3 bucket website is alive</html>" > /tmp/index.html
	awslocal s3 cp /tmp/index.html s3://${S3_ASSET_BUCKET_NAME}/index.html
	rm /tmp/index.html
	awslocal s3 website s3://${S3_ASSET_BUCKET_NAME}/ --index-document index.html
	awslocal s3api put-bucket-cors --bucket ${S3_ASSET_BUCKET_NAME} --cors-configuration file://./localstack-cors-config.json
	echo "LocalStack S3 bucket website is ready. Open http://${S3_ASSET_BUCKET_NAME}.s3-website.localhost.localstack.cloud:4566 in your browser to verify."

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
	docker compose create db
	docker compose start db
	make setup_localstack
	python scripts/seed_db.py --ciks '["0001018724", "1326801"]'  --filing_types '["10-K"]'
