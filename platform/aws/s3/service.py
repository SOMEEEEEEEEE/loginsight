import json
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

from platform.config.settings import settings
from platform.aws.s3.client import put_object, get_object


class S3Error(Exception):
    pass


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
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        put_object(
            bucket=settings.S3_BUCKET,
            key=key,
            body=body
        )

        return key

    except ClientError as e:
        raise S3Error("S3 upload failed") from e

    except Exception as e:
        raise S3Error("unexpected upload error") from e


def get_data(key: str):
    """
    Download a JSON object from S3 and parse it.
    Returns None if not found.
    """

    try:
        obj = get_object(bucket=settings.S3_BUCKET, key=key)
        raw = obj["Body"].read()

        if not raw:
            return None

        return json.loads(raw.decode("utf-8"))

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None

        raise S3Error("S3 read failed") from e

    except json.JSONDecodeError as e:
        raise S3Error("corrupted S3 data") from e