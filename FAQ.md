# Frequently Asked Questions 🔍

Here we will go over a list of commonly asked questions and/or concerns regarding this project. You may run into some of these questions yourself when reviewing the project!

## How do I add more SEC documents beyond the selected pool of SEC filings?
You can do this by using our [seed script](https://github.com/run-llama/sec-insights/tree/main/backend#seed-db-script-)!

You can run the seed script with the `--ciks` CLI arg *(e.g. `python scripts/seed_db.py --ciks '["1640147"]'`)*. The `ciks` arg allows you to define which companies you want to download SEC filings for. You can search for the CIK value for a given company using the SECs search tool on [this website](https://www.sec.gov/edgar/searchedgar/companysearch).

Alternatively, you may also just add the CIKs you want to include in your project by modifying the `DEFAULT_CIKS` list [here](https://github.com/run-llama/sec-insights/blob/main/backend/scripts/download_sec_pdf.py#L12).

Just make sure you follow the setup instructions as a pre-requisite to running the seed script :)

## How do I use different types of documents besides SEC filings? e.g. Research papers, internal documents, etc.
This can be done!

While our frontend is fairly specific to the SEC filing use-case, our backend is setup to be very flexible in terms of the types of documents you can ingest and start asking questions about.

An in-depth walkthrough on doing this can be found in [our YouTube tutorial](https://youtu.be/2O52Tfj79T4?si=kiRxB2dLES0Gaad7&t=1311).

Here are some high level steps:
1. Insert the PDF document into your database by using the script in `scripts/upsert_document.py`
   * The script will print out the newly inserted document's UUID. Make sure to copy this to your clipboard for later!
1. Start the backend service locally using `make run`
1. Start the shell-based Chat REPL using `make chat`
1. Within the REPL:
   1. First, run `pick_docs`
   1. Then run `select_id <paste the document UUID you copied earlier>` e.g. `select_id 421b8099-6155-2f6e-8c5b-674ee0ab0e7d`
   1. Type `finish` to wrap up document selection
   1. Create your conversation by typing `create`
   1. Send a message within the newly created conversation with `message <your message here>` e.g. `message What is the document about?`
      * The first time that there is a message for a newly inserted document, the backend will need to go through the embedding + indexing process for that document which can take some time.
   1. Start chatting away! The platform should now be ready for questions regarding this document within this Chat REPL.

You will also find that some of the prompts used in the application are specific to the SEC Insights use case. These will need to be changed to fit your particular use case. Here's an initial list of places in the codebase that may need to be changed to tune the prompts to your use case:
* [Custom Response Synth prompt](https://github.com/run-llama/sec-insights/blob/e81c839/backend/app/chat/qa_response_synth.py#L15-L48)
* [Vector Index tool descriptions](https://github.com/run-llama/sec-insights/blob/e81c83958a428e2aa02e8cb1280c3a17c55c4aa9/backend/app/chat/engine.py#L295-L296)
* System Message ([template](https://github.com/run-llama/sec-insights/blob/e81c83958a428e2aa02e8cb1280c3a17c55c4aa9/backend/app/chat/constants.py#L3-L17) and [construction](https://github.com/run-llama/sec-insights/blob/e81c83958a428e2aa02e8cb1280c3a17c55c4aa9/backend/app/chat/engine.py#L336))
* [User Message Prefix](https://github.com/run-llama/sec-insights/blob/e81c83958a428e2aa02e8cb1280c3a17c55c4aa9/backend/app/chat/messaging.py#L143-L145)

## How do I completely refresh my database?
During development, you may find it useful or necessary to completely wipe out your database and start fresh with empty tables.

To make this process simple, we have included a `make refresh_db` command in `backend/Makefile`. To use it, just do the following:
- `cd` into the `backend/` folder if you're not already in it
- Run `set -a` then `source .env`
   - See instructions in `README.md` for more information on what this step does
- Run `make refresh_db`
   - This will ask for confirmation first and run as soon as you type either `y` or `N`.

**What is this script doing?**

When you run the database in the `db` container using `docker compose` and the various `make` commands, the container shares a data volume with your local machine. This ensures that the data in this local database is persisted even as the `db` container is started and stopped. As such, to completely refresh this database, you would first need to stop your DB container, delete these volumes, re-create the DB container, and re-apply the alembic migrations. That's what `make refresh_db` does.
