from collections import defaultdict
import time

metrics = defaultdict(lambda: {"count": 0, "total": 0.0})

def inc(name, value=1):
    metrics[name]["count"] += value

def observe_latency(name, start_time):
    duration = time.time() - start_time
    metrics[name]["count"] += 1
    metrics[name]["total"] += duration