import boto3
import os
import uuid

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
BUCKET = os.getenv("S3_BUCKET")

if not BUCKET:
    raise ValueError("S3_BUCKET environment variable not set")

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload_log(log: str):
    key = f"logs/{uuid.uuid4()}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=log.encode("utf-8"),
        ContentType="application/json"
    )

    return key


def get_all_logs():
    logs = []

    response = s3.list_objects_v2(Bucket=BUCKET, Prefix="logs/")

    if "Contents" not in response:
        return logs

    for obj in response["Contents"]:
        data = s3.get_object(Bucket=BUCKET, Key=obj["Key"])
        logs.append(data["Body"].read().decode("utf-8"))

    return logs

def delete_all_logs():
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix="logs/")

    if "Contents" not in response:
        return

    objects = [{"Key": obj["Key"]} for obj in response["Contents"]]

    s3.delete_objects(
        Bucket=BUCKET,
        Delete={"Objects": objects}
    )