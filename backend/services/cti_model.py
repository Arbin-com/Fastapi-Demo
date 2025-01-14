from pydantic import BaseModel


class StartChannelRequest(BaseModel):
    test_name: str
    channels: list[int]


class AssignScheduleRequest(BaseModel):
    schedule_name: str
    barcode: str = ""
    capacity: float = 0
    MVUD1: float = 0
    MVUD2: float = 0
    MVUD3: float = 0
    MVUD4: float = 0
    all_assign: bool = True,
    channel_index: int = -1
