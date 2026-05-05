from shared.metrics import metrics
import time

while True:
    print("==== SYSTEM METRICS ====")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print("========================")
    time.sleep(5)