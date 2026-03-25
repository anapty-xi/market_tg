from apps.market.entities.cart_item import CartItem
from apps.market.usecases.cart.cart_usecases_protocol import CartProtocol
from util.exceptions import (
    CartItemNotExists,
    CartNotExists,
    ProductNotExists,
    UserNotExists,
)


class Base:
    def __init__(self, inf: CartProtocol):
        self.inf = inf


class GetCart(Base):
    async def execute(self, tg_id: int) -> list[CartItem]:
        if await self.inf.is_user_exists(tg_id):
            return await self.inf.get_cart_items(tg_id)
        else:
            raise UserNotExists("user does not exist")


class AddToCart(Base):
    async def execute(self, tg_id: int, prod_id: int) -> None:
        if not await self.inf.is_user_exists(tg_id):
            raise UserNotExists("user does not exist")
        if not await self.inf.is_product_exists(prod_id):
            raise ProductNotExists("product not exist")

        await self.inf.add_product(tg_id, prod_id)


class ChangeAmount(Base):
    async def execute(self, tg_id: int, prod_id: int, increase: bool = True) -> None:
        if not await self.inf.is_user_exists(tg_id):
            raise UserNotExists("user does not exist")
        if not await self.inf.is_product_exists(prod_id):
            raise ProductNotExists("product not exist")
        if not await self.inf.is_cart_item_exists(tg_id, prod_id):
            raise CartItemNotExists("cart item does not exist")

        await self.inf.change_amount(tg_id, prod_id, increase)


class DelFromCart(Base):
    async def execute(self, tg_id: int, prod_id: int) -> None:
        if not await self.inf.is_user_exists(tg_id):
            raise UserNotExists("user does not exist")
        if not await self.inf.is_product_exists(prod_id):
            raise ProductNotExists("product not exist")
        if not await self.inf.is_cart_item_exists(tg_id, prod_id):
            raise CartItemNotExists("cart item does not exist")

        await self.inf.del_from_cart(tg_id, prod_id)


class DelCart(Base):
    async def execute(self, tg_id: int) -> None:
        if await self.inf.is_cart_exists(tg_id):
            await self.inf.del_cart(tg_id)
        else:
            raise CartNotExists("cart not exist")
