from pydantic import BaseModel
from typing import Optional, List


class StructuredLog(BaseModel):
    timestamp: str
    level: str
    message: str
    service: Optional[str] = None


class LogRequest(BaseModel):
    logs: List[StructuredLog]