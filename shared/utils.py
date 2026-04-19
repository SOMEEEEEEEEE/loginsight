import uuid
import json
from typing import Any
from datetime import datetime

def generate_task_id() -> str:
    """Generate a unique UUID string for task_id."""
    return str(uuid.uuid4())

def safe_json_loads(s: str) -> Any:
    """Safely parse JSON string, return None on failure."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None

def format_timestamp(ts: datetime) -> str:
    """Return timestamp as 'YYYY-MM-DD HH:MM:SS'."""
    return ts.strftime("%Y-%m-%d %H:%M:%S")
