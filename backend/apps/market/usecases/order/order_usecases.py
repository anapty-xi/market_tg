from apps.market.entities.order import Order
from apps.market.usecases.order.order_usecases_protocol import OrderProtocol


class Base:
    def __init__(self, inf: OrderProtocol):
        self.inf = inf


class CreateOrder(Base):
    async def execute(self, tg_id: int, address: str, client_full_name: str) -> None:
        order_id = await self.inf.create_order(tg_id, address, client_full_name)
        await self.inf.create_order_items(tg_id, order_id)


class ChangeStatus(Base):
    async def execute(self, order_id: int, status: str) -> None:
        stat_map = {
            "Оплачен": "paid",
            "Неоплачен": "unpaid",
            "В пути": "on_the_way",
            "Выполнен": "done",
        }
        if status not in stat_map:
            raise ValueError("invalid status")
        await self.inf.change_status(id, order_id, stat_map[status])


class GetAllActiveOrders(Base):
    async def execute(self) -> list[Order]:
        return await self.inf.get_all_active_orders()
