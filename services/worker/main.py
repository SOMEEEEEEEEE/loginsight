"""
Current Improvements:
- Added worker runtime logging
- Added polling exception protection
- Added per-message failure isolation

Next Improvements:
- Support SQS long polling
- Add graceful shutdown handling
"""
import time
from worker.handler import handle_message
from platform.aws.sqs.consumer import receive_messages
from platform.logging.logger import get_logger

logger = get_logger("worker_main")


def main():
    logger.info("Worker started")

    while True:
        try:
            messages = receive_messages()

            if not messages:
                time.sleep(2)
                continue

            logger.info(f"Received {len(messages)} messages")

            for msg in messages:
                try:
                    handle_message(msg)

                except Exception:
                    logger.exception("Message processing failed")

        except Exception:
            logger.exception("Worker polling failed")
            time.sleep(5)


if __name__ == "__main__":
    main()