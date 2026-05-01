from pydantic import BaseModel, Field
from typing import Optional, Dict
from uuid import uuid4
from datetime import datetime


class LogEvent(BaseModel):
    """
    System-wide event contract for log processing pipeline.
    This schema is shared across ingest → SQS → worker → storage.
    """

    # --- Event metadata (system-level) ---
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    version: str = "1.0"
    source: str = Field(..., description="Origin of the event, e.g. ingest-service")

    # --- Core log fields ---
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Original log timestamp"
    )
    level: str
    message: str
    service: Optional[str] = None

    # --- Extensible metadata ---
    metadata: Optional[Dict] = Field(
        default_factory=dict,
        description="Additional structured fields (ip, latency, etc.)"
    )

    # --- Processing hints (optional, for worker use) ---
    processed: bool = False