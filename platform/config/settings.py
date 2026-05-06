import os

class Settings:
    SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 2))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))


settings = Settings()