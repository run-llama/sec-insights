# Troubleshooting
This file contains some solutions to common questions or pitfalls that may come up during development with this project.

## I'm seeing this error `pydantic.error_wrappers.ValidationError: 8 validation errors for Settings`
You may have just run a command from the `Makefile` like `make migrate` and seen an error output like this:

```
pydantic.error_wrappers.ValidationError: 8 validation errors for Settings
OPENAI_API_KEY
field required (type=value_error.missing)
AWS_KEY
field required (type=value_error.missing)
AWS_SECRET
field required (type=value_error.missing)
POLYGON_IO_API_KEY
field required (type=value_error.missing)
DATABASE_URL
field required (type=value_error.missing)
S3_BUCKET_NAME
field required (type=value_error.missing)
S3_ASSET_BUCKET_NAME
field required (type=value_error.missing)
CDN_BASE_URL
field required (type=value_error.missing)
make: *** [migrate] Error 1
```

This happens when you haven't set all the environment variables in your shell environment.
You can remedy this quickly by doing the following:
1. Create a `.env` file and source it.
   - The `.env.development` file is a good template so you can just do `cp .env.development .env`
1. `set -a`
1. `source .env`



## "Warning: Blocked access to file"

Results from a breaking change in the pdfkit library which now requires an additional
options configuraiton to enable local file access:

[See Related StackOverflow](https://stackoverflow.com/questions/62814607/pdfkit-warning-blocked-access-to-file)

```python
options = {
   "enable-local-file-access": None
}
try:
   pdfkit.from_file(input_path, output_path, verbose=True, options=options)
except Exception as e:
   print(f"Error converting {input_path} to {output_path}: {e}")
```

## OpenAI Rate Limit

When running: make seed_db_local

```bash
openai.RateLimitError: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
make: *** [Makefile:86: seed_db_local] Error 1
```