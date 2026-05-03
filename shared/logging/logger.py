import logging

logging.basicConfig(
    level=logging.INFO,
    ## SAMPLE: 2026-05-03 10:00:00 [INFO] [worker] message processed
    format="%(asctime)s [%(levelname)s] [%(service)s] %(message)s"
)

def get_logger(service):
    logger = logging.getLogger(service)

    def _log(msg, level="info"):
        extra = {"service": service}
        getattr(logger, level)(msg, extra=extra)

    return _log