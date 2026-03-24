from decimal import Decimal

from apps.market.entities.order import Order
from apps.market.entities.product import Product
from pydantic import BaseModel, ConfigDict, Field


class OrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order: Order
    product: Product
    price_at_purchase: Decimal
    quantity: int = Field(gt=0)
