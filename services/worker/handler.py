import json
import time
from worker.processor import process_logs
from platform.aws.sqs.consumer import delete_message
from platform.metrics.metrics import inc, observe_latency
from platform.logging.logger import get_logger

logger = get_logger("worker_handler")


def handle_message(msg):
    start = time.time()
    inc("message_received")

    try:
        body = json.loads(msg["Body"])

        if "logs" not in body:
            inc("message_invalid")
            raise ValueError("Invalid message format")

        process_logs(body["logs"])
        inc("message_success")
        delete_message(msg)
        inc("message_deleted")

    except Exception as e:
        inc("message_failed")
        print(f"[ERROR] Failed processing message: {e}")

    finally: 
        observe_latency("message_latency", start)