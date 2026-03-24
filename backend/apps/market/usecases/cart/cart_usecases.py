from apps.market.entities.cart_item import CartItem
from apps.market.usecases.cart.cart_usecases_protocol import CartProtocol


class Base:
    def __init__(self, inf: CartProtocol):
        self.inf = inf


class GetCart(Base):
    async def execute(self, tg_id: int) -> list[CartItem]:
        return await self.inf.get_cart_items(tg_id)


class AddToCart(Base):
    async def execute(self, tg_id: int, prod_id: int) -> None:
        await self.inf.add_product(tg_id, prod_id)


class ChangeAmount(Base):
    async def execute(self, tg_id: int, prod_id: int, increase: bool = True) -> None:
        await self.inf.change_amount(tg_id, prod_id, increase)


class DelFromCart(Base):
    async def execute(self, tg_id: int, prod_id: int) -> None:
        await self.inf.del_from_cart(tg_id, prod_id)


class DelCart(Base):
    async def execute(self, tg_id: int) -> None:
        await self.inf.del_cart(tg_id)
