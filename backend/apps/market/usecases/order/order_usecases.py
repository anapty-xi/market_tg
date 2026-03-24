from apps.market.usecases.order.order_usecases_protocol import OrderProtocol


class Base:
    def __init__(self, inf: OrderProtocol):
        self.inf = inf


class CreateOrder(Base):
    async def execute(self, tg_id: int, address: str, client_full_name: str) -> None:
        order_id = await self.inf.create_order(tg_id)
        await self.inf.create_order_items(tg_id, order_id)


class ChangeStatus(Base):
    async def execute(self, id: int, status: str) -> None:
        if status not in ["Оплачен", "Неоплачен", "В пути", "Выполнен"]:
            raise ValueError("invalid status")
        await self.inf.change_status(id, status)


class GetAllActiveOrders(Base):
    async def execute(self) -> dict:
        return await self.inf.get_all_active_orders()
