from datetime import datetime
from worker.analyzer import analyze_logs
from worker.validator import validate_logs
from worker.storage import save_result, save_raw


def process_logs(logs: list, task_id: str):

    structured_logs = validate_logs(logs)

    inc("logs_validated")

    result = analyze_logs(structured_logs)

    inc("analysis_done")

    save_result(task_id, result)
    save_raw(task_id, structured_logs)