from decimal import Decimal

from entities.order import Order
from entities.product import Product
from pydantic import BaseModel, ConfigDict, Field


class OrderItem(BaseModel):
    conf = ConfigDict(from_attributes=True)

    id: int
    order: Order
    product: Product
    price_at_purchase: Decimal
    quantity: int = Field(gt=0)
