import json
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from shared.config.settings import settings
from shared.aws.s3.client import put_object, get_object

def upload_data(data: dict) -> str:
    """
    Upload JSON data to S3 and return object key.
    """
    key = (
        f"results/"
        f"{datetime.utcnow().strftime('%Y/%m/%d')}/"
        f"{uuid.uuid4()}.json"
    )

    try:
        put_object(
            bucket=settings.S3_BUCKET,
            key=key,
            body=json.dumps(data).encode("utf-8")
        )
    except Exception as e:
        print(f"[ERROR] upload_data failed: {e}")
        raise

    return key

def get_data(key: str):
    """
    Download a JSON object from S3 and parse it.
    Returns None if not found.
    """
    try:
        obj = get_object(
            bucket=settings.S3_BUCKET,
            key=key
        )

        return json.loads(obj["Body"].read().decode("utf-8"))

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise