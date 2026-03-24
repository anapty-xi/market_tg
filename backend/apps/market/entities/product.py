from decimal import Decimal

from entities.category import Category
from pydantic import BaseModel, ConfigDict, Field


class Product(BaseModel):
    conf = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(max_length=128)
    description: None | str
    price: Decimal
    category: Category
