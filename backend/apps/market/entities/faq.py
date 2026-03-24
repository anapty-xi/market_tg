from pydantic import BaseModel, ConfigDict, Field


class FAQ(BaseModel):
    conf = ConfigDict(from_attributes=True)

    id: int
    question: str = Field(max_length=255)
    answer: str
    active: bool = True
