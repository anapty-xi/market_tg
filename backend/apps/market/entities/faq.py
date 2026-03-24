from pydantic import BaseModel, ConfigDict, Field


class FAQ(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question: str = Field(max_length=255)
    answer: str
    active: bool = True
