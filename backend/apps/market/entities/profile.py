from pydantic import BaseModel, ConfigDict, Field


class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_id: int
    username: None | str = Field(max_length=128)
    phone_number: None | str = Field(max_length=16, default=None)
