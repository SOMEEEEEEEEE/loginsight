from collections import Counter
import re

def analyze_logs(logs):
    # Filter out logs
    error_logs = [log for log in logs if "ERROR" in log]
    patterns = [extract_pattern(log) for log in error_logs]
    counter = Counter(patterns)

    # Simple error analyses
    top_errors = [p for p, _ in counter.most_common(3)]
    error_rate = len(error_logs) / len(logs) if logs else 0
    # Use error rate as a simple anomaly score
    anomaly_score = round(error_rate, 2)

    # Return results
    return {
        "error_count": len(error_logs),
        "top_errors": top_errors,
        "anomaly_score": anomaly_score
    }

# Function to clean and extract pattern from a log line
def extract_pattern(log):
    # Remove numbers & "ERROR", strip spaces
    return re.sub(r'\d+', '', log).replace("ERROR", "").strip()