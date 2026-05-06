import logging
import json

logging.basicConfig(level=logging.INFO)

def get_logger(service):
    logger = logging.getLogger(service)

    def log(message, **kwargs):
        payload = {
            "service": service,
            "message": message,
            **kwargs
        }
        logger.info(json.dumps(payload))

    return log