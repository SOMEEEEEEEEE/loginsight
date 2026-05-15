import signal
import threading
from platform.logging.logger import get_logger

logger = get_logger("worker_shutdown")

stop_event = threading.Event()


def handle_shutdown(signum, frame):
    logger.info(
        "Shutdown signal received",
        extra={"signal": signum}
    )
    stop_event.set()


def register_signals():
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)