from apps.market.entities.order import Order
from apps.market.usecases.order.order_usecases_protocol import OrderProtocol
from util.exceptions import CartNotExists, InvalidStatus, OrderNotExists, UserNotExists


class Base:
    def __init__(self, inf: OrderProtocol):
        self.inf = inf


class CreateOrder(Base):
    async def execute(
        self, tg_id: int, address: str, client_full_name: str
    ) -> None | Exception:
        if await self.inf.is_user_exists(tg_id):
            if await self.inf.has_cart(tg_id):
                order_id = await self.inf.create_order(tg_id, address, client_full_name)
                await self.inf.create_order_items(tg_id, order_id)
                await self.inf.del_cart(tg_id)
            else:
                raise CartNotExists("user does not have cart")
        else:
            raise UserNotExists("user does not exist")


class ChangeStatus(Base):
    async def execute(self, order_id: int, status: str) -> None:
        if not await self.inf.is_order_exists(order_id):
            raise OrderNotExists("order does not existst")

        stats = ["paid", "unpaid", "on_the_way", "done"]
        if status not in stats:
            raise InvalidStatus("invalid status")
        await self.inf.change_status(order_id, status)


class GetAllActiveOrders(Base):
    async def execute(self) -> list[Order]:
        return await self.inf.get_all_active_orders()
