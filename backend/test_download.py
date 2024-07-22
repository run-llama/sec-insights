import s3fs
import os
from urllib.parse import urlparse

s3 = s3fs.S3FileSystem(
    key="AKIAU6GDV5W75F76ITHP",
    secret="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",
    endpoint_url="https://sec-insights-local.s3.amazonaws.com",
)

def download_file_from_url(url, local_path):
    # Parse the URL to get the S3 path
    parsed_url = urlparse(url)
    s3_path = parsed_url.path.lstrip('/')
    
    # Create the local directory if it doesn't exist
    local_dir = os.path.dirname(local_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    # Download the file from S3 to the local path
    print(f"Downloading {s3_path} to {local_path}")
    s3.get(s3_path, local_path)

# Example usage
url = "https://sec-insights-local.s3.amazonaws.com/sec-edgar-filings/0001018724/10-Q/0001018724-23-000018/primary-document.pdf"
local_path = "/root/new_folder/sec-edgar-filings_new/0001018724/10-Q/0001018724-23-000018/primary-document.pdf"

download_file_from_url(url, local_path)
