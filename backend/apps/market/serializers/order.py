from apps.market.entities.order import Order
from pydantic import ConfigDict


class ProductOut(Order):
    model_config = ConfigDict(from_attributes=True)

    prods: list[str]
