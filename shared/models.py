from pydantic import BaseModel
from typing import Optional, List, Dict

# Pydantic model for a single log
class StructuredLog(BaseModel):
    timestamp: str
    level: str
    message: str
    service: Optional[str] = None

# Model for batch submission
class LogRequest(BaseModel):
    logs: List[StructuredLog]