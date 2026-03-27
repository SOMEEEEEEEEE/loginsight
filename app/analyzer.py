from collections import Counter
import re

TOP_ERROR = 3

def analyze_logs(logs):
    # Filter out logs
    error_logs = [log for log in logs if log.level.upper() == "ERROR"]
    patterns = [log.message.strip() for log in error_logs]

    counter = Counter(patterns)

    # Simple error analyses -> return top TOP_ERROR errors
    top_errors = [p for p, _ in counter.most_common(TOP_ERROR)]
    error_rate = len(error_logs) / len(logs) if logs else 0

    # Use error rate as a simple anomaly score
    anomaly_score = round(error_rate, 2)

    return {
        "error_count": len(error_logs),
        "top_errors": top_errors,
        "anomaly_score": anomaly_score
    }


# Function to clean and extract pattern from a unstructured log line
def extract_pattern(log):
    # Extract only error info
    match = re.search(r"ERROR[:\s]*(.*)", log)
    if match:
        return match.group(1).strip()
    # Fallback, return origin log
    return log