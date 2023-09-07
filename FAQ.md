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
