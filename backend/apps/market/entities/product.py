from decimal import Decimal

from apps.market.entities.category import Category
from pydantic import BaseModel, ConfigDict, Field


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(max_length=128)
    description: None | str
    price: Decimal
    category: Category
