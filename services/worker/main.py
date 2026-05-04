"""
  Control the main loop. 
"""
import time
from shared.aws.sqs.consumer import receive_messages
from worker.handler import handle_message

def main():
    while True:
        messages = receive_messages()

        if not messages:
            time.sleep(2)
            continue

        for msg in messages:
            handle_message(msg)


if __name__ == "__main__":
    main()