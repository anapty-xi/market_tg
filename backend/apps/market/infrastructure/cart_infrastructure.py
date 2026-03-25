from apps.market.entities.cart_item import CartItem
from apps.market.models import CartItem as DBItem
from apps.market.models import Profile
from apps.market.usecases.cart.cart_usecases_protocol import CartProtocol


class CartDBGW(CartProtocol):
    async def get_cart_items(self, tg_id: int) -> list[CartItem]:
        user = await Profile.objects.aget(tg_id=tg_id)
        orm_items = DBItem.objects.select_related("product").filter(user=user)
        return [CartItem.model_validate(item) async for item in orm_items]

    async def add_product(self, tg_id: int, prod_id: int) -> None:
        await DBItem.objects.acreate(user__id=tg_id, product__id=prod_id, quantity=1)

    async def change_amount(self, tg_id: int, prod_id: int, increase: bool) -> None:
        item = await DBItem.objects.select_related("product").aget(
            user__tg_id=tg_id, product__id=prod_id
        )
        if increase:
            item.quantity += 1
        else:
            if item.quantity > 1:
                item.quantity -= 1

        if item.quantity > 0:
            await item.asave()
        else:
            await item.adelete()

    async def del_from_cart(self, tg_id: int, prod_id: int) -> None:
        await DBItem.objects.aget(user__tg_id=tg_id, product__id=prod_id).adelete()

    async def del_cart(self, tg_id: int):
        await DBItem.objects.filter(user__tg_id=tg_id).adelete()
