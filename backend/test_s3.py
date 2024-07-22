import s3fs

s3 = s3fs.S3FileSystem(
    key="AKIAU6GDV5W75F76ITHP",
    secret="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",
    endpoint_url=None,
)

try:
    buckets = s3.ls('')
    print("Buckets:", buckets)
except Exception as e:
    print("Error:", e)


# import s3fs
# import os

# s3 = s3fs.S3FileSystem(
#     key="AKIAU6GDV5W75F76ITHP",
#     secret="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",
#     # endpoint_url=None
#     endpoint_url="https://sec-insights-local.s3.amazonaws.com",
# )

# s3_bucket = "sec-edgar-filings"

# if not s3.exists(s3_bucket):
#     print("Bucket not found, creating bucket")
#     s3.mkdir(s3_bucket)

# dir_path = "/root/mounted_folder/sec-edgar-filings"

# def upload_directory(local_path, s3_path):
#     for root, dirs, files in os.walk(local_path):
#         for file in files:
#             local_file = os.path.join(root, file)
#             s3_file = os.path.join(s3_path, os.path.relpath(local_file, local_path))
#             print(f"Uploading {local_file} to {s3_file}")
#             s3.put(local_file, s3_file)

# upload_directory(dir_path, s3_bucket)

