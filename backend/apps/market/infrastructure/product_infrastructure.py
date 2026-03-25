from apps.market.usecases.product.product_usecases_protocol import ProductProtocol
from apps.market.entities.category import Category
from apps.market.entities.product import Product
from apps.market.models import Product as DBProd, Category as DBCat


class ProductDBGW(ProductProtocol):
    async def get_products(self) -> list[Product]:
        orm_products = DBProd.objects.select_related('category').all()
        return [Product.model_validate(pr) async for pr in orm_products]
    
    async def get_categories(self) -> list[Category]:
        orm_categories = DBCat.objects.all()
        return [Category.model_validate(cat) async for cat in orm_categories]

