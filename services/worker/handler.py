import json
import time
from worker.processor import process_logs
from shared.aws.sqs.consumer import delete_message
from shared.metrics import inc, observe_latency

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