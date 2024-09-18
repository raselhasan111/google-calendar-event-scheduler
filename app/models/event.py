from pydantic import BaseModel
from typing import Optional, List


class Event(BaseModel):
    summary: str
    description: Optional[str] = None
    start: dict
    end: dict
    location: Optional[str] = None
    attendees: Optional[List[str]] = None
