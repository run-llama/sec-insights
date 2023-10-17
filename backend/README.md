# SEC Insights Backend
Live at https://secinsights.ai/
## Setup Dev Workspace
1. Install [pyenv](https://github.com/pyenv/pyenv#automatic-installer) and then use it to install the Python version in `.python-version`.
    1. install pyenv with `curl https://pyenv.run | bash`
    * This step can be skipped if you're running from the devcontainer image in Github Codespaces
1. [Install docker](https://docs.docker.com/engine/install/)
    * This step can be skipped if you're running from the devcontainer image in Github Codespaces
1. Run `poetry shell`
1. Run `poetry install` to install dependencies for the project
1. Create the `.env` file and source it. The `.env.development` file is a good template.
    1. `cp .env.development .env`
    1. `set -a`
    1. `source .env`
1. Run the database migrations with `make migrate`
1. Run `make run` to start the server locally
    - This spins up the Postgres 15 DB & Localstack in their own docker containers.
    - The server will not run in a container but will instead run directly on your OS.
        - This is to allow for use of debugging tools like `pdb`
1. Lastly, you will likely want to populate your local database with some sample SEC filings
    - We have a script for this! But first, open your `.env` file and replace the placeholder value for the `OPENAI_API_KEY` with your own OpenAI API key
        - At some point you will want to do the same for the other secret keys in here like `POLYGON_IO_API_KEY`, `AWS_KEY`, & `AWS_SECRET`
        - To follow the [SEC's Internet Security Policy](https://www.sec.gov/os/webmaster-faq#code-support), make sure to also replace the `SEC_EDGAR_COMPANY_NAME` & `SEC_EDGAR_EMAIL` values in the `.env` file with your own values.
    - Source the file again with `set -a` then `source .env`
    - Run `make seed_db_local`
        - If this step fails, you may find it helpful to run `make refresh_db` to wipe your local database and re-start with emptied tables.
    - Done 🏁! You can run `make run` again and you should see some documents loaded at http://localhost:8000/api/document

For any issues in setting up the above or during the rest of your development, you can check for solutions in the following places:
- [`backend/troubleshooting.md`](https://github.com/run-llama/sec-insights/blob/main/backend/troubleshooting.md)
- [Open & already closed Github Issues](https://github.com/run-llama/sec-insights/issues?q=is%3Aissue+is%3Aclosed)
- The [#sec-insights discord channel](https://discord.com/channels/1059199217496772688/1150942525968879636)

## Scripts
The `scripts/` folder contains several scripts that are useful for both operations and development.

## Chat 🦙
The script at `scripts/chat_llama.py` spins up a repl interface to start a chat within your terminal by interacting with the API directly. This is useful for debugging issues without having to interact with a full frontend.

The script takes an optional `--base_url` argument that defaults to `http://localhost:8000` but can be specified to make the script point to the prod or preview servers. The `Makefile` contains `chat` & `chat_prod` commands that specify this arg for you.

Usage is as follows:

```
$ poetry shell  # if you aren't already in your poetry shell
$ make chat
poetry run python -m scripts.chat_llama
(Chat🦙) create
Created conversation with ID 8371bbc8-a7fd-4b1f-889b-d0bc882df2a5
(Chat🦙) detail
{
    "id": "8371bbc8-a7fd-4b1f-889b-d0bc882df2a5",
    "created_at": "2023-06-29T20:50:21.330170",
    "updated_at": "2023-06-29T20:50:21.330170",
    "messages": []
}
(Chat🦙) message Hi


=== Message 0 ===
{'id': '05db08be-bbd5-4908-bd68-664d041806f6', 'created_at': None, 'updated_at': None, 'conversation_id': '8371bbc8-a7fd-4b1f-889b-d0bc882df2a5', 'content': 'Hello! How can I assist you today?', 'role': 'assistant', 'status': 'PENDING', 'sub_processes': [{'id': None, 'created_at': None, 'updated_at': None, 'message_id': '05db08be-bbd5-4908-bd68-664d041806f6', 'content': 'Starting to process user message', 'source': 'constructed_query_engine'}]}


=== Message 1 ===
{'id': '05db08be-bbd5-4908-bd68-664d041806f6', 'created_at': '2023-06-29T20:50:36.659499', 'updated_at': '2023-06-29T20:50:36.659499', 'conversation_id': '8371bbc8-a7fd-4b1f-889b-d0bc882df2a5', 'content': 'Hello! How can I assist you today?', 'role': 'assistant', 'status': 'SUCCESS', 'sub_processes': [{'id': '75ace83c-1ebd-4756-898f-1957a69eeb7e', 'created_at': '2023-06-29T20:50:36.659499', 'updated_at': '2023-06-29T20:50:36.659499', 'message_id': '05db08be-bbd5-4908-bd68-664d041806f6', 'content': 'Starting to process user message', 'source': 'constructed_query_engine'}]}


====== Final Message ======
Hello! How can I assist you today?
```

## SEC Document Downloader 📃
We have a script to easily download SEC 10-K & 10-Q files! This is a single step of the larger seed script described in the next section. Unless you have some use for just running this step on it's own, you probably want to stick to the Seed script described in the section below 🙂
However, the setup instructions for this script are a pre-requisite for running the seed script.

No API keys are needed to use this, it calls the SEC's free to use Edgar API.

The instructions below explain a process to use the script to download the SEC filings, convert the to PDFs, and store them in an S3 bucket.

### Setup / Usage Instructions
Pre-requisite setup steps to use the downloader script to load the SEC PDFs directly into an S3 bucket.

These steps assume you've already followed the steps above for setting up your dev workspace!

1. Setup AWS CLI
    1. Install AWS CLI
        - This step can be skipped if you're running from the devcontainer image in Github Codespaces
        - Steps:
            - `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`
            - `unzip awscliv2.zip`
            - `sudo ./aws/install`
    1. Configure AWS CLI
        - This is mainly to set the AWS credentials that will later be used by s3fs
        - Run `aws configure` and enter the access key & secret key for a AWS IAM user that has access to the PDFs where you want to store the SEC files.
            - set the default AWS region to `us-east-1` (what we're primarily using).
1. Setup [`s3fs`](https://github.com/s3fs-fuse/s3fs-fuse)
    1. Install s3fs
        - This step can be skipped if you're running from the devcontainer image in Github Codespaces
        - `sudo apt install s3fs`
    1. Setup a s3fs mounted folder
        - Create the mounted folder locally `mkdir ~/mounted_folder`
        - `s3fs llama-app-web-assets-preview ~/mounted_folder`
            - You can replace `llama-app-web-assets-preview` with the name of the S3 bucket you want to upload the files to.
1. Install [`wkhtmltopdf`](https://wkhtmltopdf.org/)
    - This step can be skipped if you're running from the devcontainer image in Github Codespaces
    - Steps:
        - `sudo apt-get update`
        - `sudo apt-get install wkhtmltopdf`
1. Get into your poetry shell with `poetry shell` from the project's root directory.
1. Run the script! `python scripts/download_sec_pdf.py -o ~/mounted_folder --file-types="['10-Q','10-K']"`
    - Take a 🚽 break while it's running, it'll take a while!
1. Go to AWS Console and verify you're seeing the SEC files in the S3 bucket.

## Seed DB Script 🌱
There are a collection of scripts we have for seeding the database with a set of documents.
The script in `scripts/seed_db.py` is an attempt at consolidating those disparate scripts into one unified command.

This script will:
1. Download a set of SEC 10-K & 10-Q documents to a local temp directory
1. Upload those SEC documents to the S3 folder specified by `$S3_ASSET_BUCKET_NAME`
1. Crawl through all the PDF files in the S3 folder and upsert a database row into the Document table based on the path of the file within the bucket

### Use Cases
This is useful for times when:
1. You want to setup a local environment with your local Postgres DB to have a set of documents in the `documents` table
    * When running locally, this will use [`localstack`](https://localstack.cloud/) to store the documents into a local S3 bucket instead of a real one.
1. You want to update the documents present in either Prod or Preview DBs
    * In fact, this is the very script that is run by the [`llama-app-cron` cron job service](https://github.com/run-llama/sec-insights/blob/294d8e5/render.yaml#L38) that gets setup by the `render.yaml` blueprint when deploying this service to Render.com.

### Usage
To run the script, make sure you've:
1. Activated your Python virtual environment using `poetry shell`
1. Installed all the pre-requisite dependencies for the `SEC Document Downloader` script.
1. Defined all the environment variables from `.env.development` within your shell environment according to the environment you want to execute the seed script (e.g. local, preview, prod environments)

After that you can run `python scripts/seed_db.py` to start the seed process.

To make things easier, the Makefile has some shorthand commands.
1. `make seed_db`
    - Just runs the `seed_db.py` script with no CLI args, so just based on what env vars you've set
1. `make seed_db_preview`
    - Same as `make seed_db` but only loads SEC documents from Amazon & Meta
    - We don't need to load that many company documents for Preview environments.
1. `make seed_db_local`
    - To be used for local database seeding
    - Runs `seed_db.py` just for $AMZN & $META documents
    - Sets up the localstack bucket to actually serve the documents locally as well, so you can load them in your local browser.
1. `make seed_db_based_on_env`
    - Automatically calls one of the above shorthands based on the `RENDER` & `IS_PREVIEW_ENV` environment variables
