from apps.market.entities.category import Category
from apps.market.entities.product import Product
from apps.market.usecases.product.product_usecases_protocol import ProductProtocol


class Base:
    def __init__(self, inf: ProductProtocol):
        self.inf = inf


class GetProducts(Base):
    async def execute(self) -> list[Product]:
        list_products = await self.inf.get_products()
        return [Product(**prod) for prod in list_products]


class GetCategories(Base):
    async def execute(self) -> list[Category]:
        list_categories = await self.inf.get_categories()
        return [Category(**cat) for cat in list_categories]
