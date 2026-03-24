from pydantic import BaseModel, ConfigDict, Field


class Category(BaseModel):
    conf = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(max_length=128)
    parent: None | "Category" = None
