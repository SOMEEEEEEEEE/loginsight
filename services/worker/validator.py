"""
Initialization: Decoupled validation from processor.py for a clearer structure
"""
from platform.contracts.log_request import StructuredLog

def validate_logs(raw_logs):
    valid = []

    for log in raw_logs:
        try:
            valid.append(StructuredLog(**log))
        except Exception:
            logger.warning("Invalid log skipped")
            inc("log_validation_failed")

    return valid