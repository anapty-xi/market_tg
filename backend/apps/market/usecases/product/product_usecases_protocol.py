from typing import Protocol

from apps.market.entities.category import Category
from apps.market.entities.product_image import ProductImage


class ProductProtocol(Protocol):
    async def get_main_categories(self) -> list[Category]: ...
    async def get_sub_categories(self, main_cat_id: int) -> list[Category]: ...
    async def get_products(self, cat_id: int) -> list[ProductImage]: ...
