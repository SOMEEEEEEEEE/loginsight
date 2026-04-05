from common.s3_service import download_json

def get_result(task_id: str):
    """
    Receives a task_id and uses it to query a result in S3.
    """
    key = f"results/{task_id}.json"
    result = download_json(key)
    if result is None:
        return {"task_id": task_id, "status": "processing"}
    return {"task_id": task_id, "status": "completed", "result": result}