from apps.market.entities.product import Product
from pydantic import BaseModel, ConfigDict


class ProductImage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product: Product
    image: str
