"""
Current Improvements:
- Added worker runtime logging
- Added polling exception protection
- Added per-message failure isolation
- Added configurable polling interval support
- Added SQS long polling
- Added structured error logging for worker failures

Next Improvements:
- Add graceful shutdown handling
"""
import time
from worker.handler import handle_message
from platform.aws.sqs.consumer import receive_messages
from platform.logging.logger import get_logger
from platform.config.settings import settings

logger = get_logger("worker_main")


def main():
    logger.info("Worker started")

    while True:
        try:
            messages = receive_messages()

            if not messages:
                time.sleep(settings.POLL_INTERVAL)
                continue

            logger.info(
                "Received messages",
                extra={"count": len(messages)}
            )

            for msg in messages:
                try:
                    handle_message(msg)

                except Exception as e:
                    logger.exception(
                        "Message processing failed",
                        extra={
                            "error": str(e),
                            "message_id": msg.get("MessageId")
                        }
                    )

        except Exception as e:
            logger.exception(
                "Worker polling failed",
                extra={
                    "error": str(e)
                }
            )
            time.sleep(settings.POLL_INTERVAL)


if __name__ == "__main__":
    main()