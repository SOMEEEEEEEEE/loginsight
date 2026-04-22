import uuid
import json
from datetime import datetime
from botocore.exceptions import ClientError
from shared.s3_client import s3, BUCKET


def upload_with_key(key: str, data: dict):
    try:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(data).encode("utf-8"),
            ContentType="application/json"
        )
    except Exception as e:
        print(f"[ERROR] Failed to upload data: {e}")
        raise

    return key

def upload_data(data: dict):
    """
    Upload JSON data to S3 and return object key.
    """

    # Update the key to a date-bound format
    key = f"results/{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4()}.json"

    try:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(data).encode("utf-8"),
            ContentType="application/json"
        )
    except Exception as e:
        print(f"[ERROR] Failed to upload data: {e}")
        raise

    return key


def get_data(key: str):
    """
    Download a JSON object from S3 and parse it.
    Returns None if not found.
    """
    try:
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        return json.loads(obj["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise