import logging
import json
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)


def get_logger(service: str):
    logger = logging.getLogger(service)

    def log(event, **kwargs):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service,
            "event": event,
            "meta": kwargs
        }

        logger.info(json.dumps(payload))

    return log