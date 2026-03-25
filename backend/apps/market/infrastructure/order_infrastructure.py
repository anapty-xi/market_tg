from apps.market.entities.order import Order as EntityOrder
from apps.market.models import CartItem, Order, OrderItem, Profile
from apps.market.usecases.order.order_usecases_protocol import OrderProtocol


class OrderDBGW(OrderProtocol):
    async def create_order(
        self, tg_id: int, address: str, client_full_name: str
    ) -> int:
        order = await Order.objects.acreate(
            status="unpaid",
            client_id=tg_id,
            client_full_name=client_full_name,
            address=address,
        )
        return order.id

    async def create_order_items(self, tg_id: int, order_id: str) -> None:
        cart_items = CartItem.objects.select_related("product").filter(
            user__tg_id=tg_id
        )
        async for item in cart_items:
            await OrderItem.objects.acreate(
                order_id=order_id,
                product=item.product,
                price_at_purchase=item.product.price,
                quantity=item.quantity,
            )

    async def change_status(self, order_id: int, status: str) -> None:
        order = await Order.objects.aget(id=order_id)
        order.status = status
        await order.asave()

    async def get_all_active_orders(self) -> list[Order]:
        orders_orm = Order.objects.select_related("client").exclude(status="done")
        return [EntityOrder.model_validate(ord) async for ord in orders_orm]

    async def del_cart(self, tg_id: int):
        await CartItem.objects.filter(user__tg_id=tg_id).adelete()

    async def has_cart(self, tg_id: int) -> bool:
        items = [item async for item in CartItem.objects.filter(user__tg_id=tg_id)]
        return len(items) > 0

    async def is_user_exists(self, tg_id: int) -> bool:
        try:
            await Profile.objects.aget(tg_id=tg_id)
            return True
        except Exception:
            return False

    async def is_order_exists(self, order_id: int) -> bool:
        try:
            await Order.objects.aget(id=order_id)
            return True
        except Exception:
            return False
