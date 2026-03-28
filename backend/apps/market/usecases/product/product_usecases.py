from apps.market.entities.category import Category
from apps.market.serializers.product import ProductOut
from apps.market.usecases.product.product_usecases_protocol import ProductProtocol


class Base:
    def __init__(self, inf: ProductProtocol):
        self.inf = inf


class GetProducts(Base):
    async def execute(self, cat_id: int) -> list[ProductOut]:
        return await self.inf.get_products(cat_id)


class GetMainCategories(Base):
    async def execute(self) -> list[Category]:
        return await self.inf.get_main_categories()


class GetSubCategories(Base):
    async def execute(self, main_cat_id: int) -> list[Category]:
        return await self.inf.get_sub_categories(main_cat_id)
