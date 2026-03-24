from pydantic import BaseModel, ConfigDict, Field


class Subscription(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(max_length=64)
    channel_id: str = Field(max_length=128)
    link: str = Field(max_length=128)
