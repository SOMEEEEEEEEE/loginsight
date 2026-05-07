import logging
import json
import time

logging.basicConfig(level=logging.INFO)


def get_logger(service):
    logger = logging.getLogger(service)

    def log(event, **kwargs):
        payload = {
            "timestamp": round(time.time(), 2),
            "service": service,
            "event": event,
            **kwargs
        }

        logger.info(json.dumps(payload))

    return log