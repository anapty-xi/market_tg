from apps.market.entities.category import Category
from apps.market.models import Category as DBCat
from apps.market.models import Product as DBProd
from apps.market.serializers.product import ProductOut
from apps.market.usecases.product.product_usecases_protocol import ProductProtocol


class ProductDBGW(ProductProtocol):
    async def get_products(self, cat_id: int) -> list[ProductOut]:
        if cat_id == 0:
            orm_products = (
                DBProd.objects.select_related("category", "category__parent")
                .prefetch_related("images")
                .all()
            )
        else:
            orm_products = (
                DBProd.objects.filter(category_id=cat_id)
                .select_related("category", "category__parent")
                .prefetch_related("images")
            )

        products = []
        async for prod in orm_products:
            prod.images_links = [img.image.url for img in prod.images.all()]
            products.append(prod)

        return [ProductOut.model_validate(prod) for prod in products]

    async def get_main_categories(self) -> list[Category]:
        orm_categories = DBCat.objects.filter(parent__isnull=True)
        return [Category.model_validate(cat) async for cat in orm_categories]

    async def get_sub_categories(self, main_cat_id: int) -> list[Category]:
        if main_cat_id == 0:
            orm_subcategories = DBCat.objects.select_related("parent").filter(
                parent__isnull=False
            )
        else:
            orm_subcategories = DBCat.objects.select_related("parent").filter(
                parent_id=main_cat_id
            )
        return [Category.model_validate(subcat) async for subcat in orm_subcategories]
