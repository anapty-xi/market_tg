from datetime import datetime

from entities.profile import Profile
from pydantic import BaseModel, ConfigDict, Field


class Order(BaseModel):
    conf = ConfigDict(from_attributes=True)

    id: int
    status: str = "unpaid"
    client: Profile
    address: str
    client_full_name: str = Field(max_length=128)
    created_at: datetime
