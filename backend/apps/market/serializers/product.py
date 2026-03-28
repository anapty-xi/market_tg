from apps.market.entities.product import Product
from pydantic import ConfigDict


class ProductOut(Product):
    model_config = ConfigDict(from_attributes=True)

    images_links: list[str] = None
