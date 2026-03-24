from typing import Protocol

from apps.market.entities.category import Category
from apps.market.entities.product import Product


class ProductProtocol(Protocol):
    async def get_products(self) -> list[Product]: ...
    async def get_categories(self) -> list[Category]: ...
