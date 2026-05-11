"""
Current improvements:
- Added normalized error pattern extraction
- Improved top error aggregation with frequency counts
- Added total_logs and error_rate analytics metrics
- Enhanced anomaly scoring based on error density
"""

from collections import Counter
import re

TOP_ERROR = 3


def analyze_logs(logs):

    error_logs = [
        log for log in logs
        if log.level.upper() == "ERROR"
    ]

    patterns = [
        extract_pattern(log.message)
        for log in error_logs
    ]

    counter = Counter(patterns)

    top_errors = [
        {
            "pattern": pattern,
            "count": count
        }
        for pattern, count in counter.most_common(TOP_ERROR)
    ]

    error_rate = len(error_logs) / len(logs) if logs else 0

    anomaly_score = round(error_rate, 2)

    return {
        "total_logs": len(logs),
        "error_count": len(error_logs),
        "error_rate": round(error_rate, 2),
        "top_errors": top_errors,
        "anomaly_score": anomaly_score
    }


def extract_pattern(message: str) -> str:

    match = re.search(r"ERROR[:\s]*(.*)", message)

    if match:
        pattern = match.group(1).strip()

        # normalize dynamic IDs/numbers
        pattern = re.sub(r"\d+", "<NUM>", pattern)

        return pattern

    return message.strip()