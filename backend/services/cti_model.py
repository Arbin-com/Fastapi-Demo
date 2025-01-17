from pydantic import BaseModel
from typing import Optional, Any


class StartChannelRequest(BaseModel):
    test_name: str
    channels: list[int]


class StopChannelRequest(BaseModel):
    channel_index: int
    is_stop_all: bool = False


class StopChannelResponse(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None
    feedback: Optional[Any] = None


class AssignScheduleRequest(BaseModel):
    schedule_name: str
    barcode: str = ""
    capacity: float = 0.0
    MVUD1: float = 0.0
    MVUD2: float = 0.0
    MVUD3: float = 0.0
    MVUD4: float = 0.0
    all_assign: bool = False
    channel_index: int = -1
