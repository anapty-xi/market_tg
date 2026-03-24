from apps.market.entities.category import Category
from apps.market.entities.product import Product
from apps.market.usecases.product.product_usecases_protocol import ProductProtocol


class Base:
    def __init__(self, inf: ProductProtocol):
        self.inf = inf


class GetProducts(Base):
    async def execute(self) -> list[Product]:
        return await self.inf.get_products()


class GetCategories(Base):
    async def execute(self) -> list[Category]:
        return await self.inf.get_categories()
