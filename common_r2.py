"""Shared helper: upload a finished file to R2 and return its public link (same settings as the other workers)."""
import os
import boto3


def upload_to_r2(local_path, key, content_type):
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY"],
        aws_secret_access_key=os.environ["R2_SECRET_KEY"],
        region_name="auto",
    )
    s3.upload_file(local_path, os.environ["R2_BUCKET"], key, ExtraArgs={"ContentType": content_type})
    return f"{os.environ['R2_PUBLIC_URL'].rstrip('/')}/{key}"
