from pydantic import BaseModel


class StartChannelRequest(BaseModel):
    test_name: str
    channels: list[int]
