from pydantic import BaseModel
from typing import Optional, Any


class LoginRequest(BaseModel):
    username: str
    password: str
    ipaddress: str
    port: int = 9031  # Port assigned for CTI communication


class StartChannelRequest(BaseModel):
    test_name: str
    channels: list[int]


class StopChannelRequest(BaseModel):
    channel_index: int
    is_stop_all: bool = False


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


class AssignFileRequest(BaseModel):
    file_name: str
    all_assign: bool = False
    file_type: int
    channels: list[int]
