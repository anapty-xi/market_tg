import json

from apps.market.entities.order import Order as EntityOrder
from apps.market.models import CartItem, Order, OrderItem, Profile
from apps.market.usecases.order.order_usecases_protocol import OrderProtocol
from django.conf import settings


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

    async def get_all_active_orders(self) -> list[dict]:
        orders_orm = (
            Order.objects.select_related("client")
            .prefetch_related("items", "items__product")
            .exclude(status="done")
        )
        orders_list = []
        async for order in orders_orm:
            order_dict = EntityOrder.model_validate(order).model_dump()
            order_dict["items"] = [
                {
                    "name": p.product.name,
                    "price_at_purchasece": p.price_at_purchase,
                    "quantity": p.quantity,
                }
                async for p in order.items.all()
            ]
            orders_list.append(order_dict)
        return orders_list

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

    async def notify_admin(self, order_id: int) -> None:
        r = settings.REDIS_OBJ
        order = await Order.objects.select_related("client").aget(id=order_id)

        items = OrderItem.objects.select_related("product").filter(order=order_id)

        items_list = [
            {
                "name": item.product.name,
                "price_at_purchasece": str(item.price_at_purchase),
                "quantity": item.quantity,
            }
            async for item in items
        ]

        payload = {
            "order_id": order.id,
            "status": order.status,
            "client_name": order.client_full_name,
            "address": order.address,
            "items": items_list,
        }

        await r.lpush("order_notifications", json.dumps(payload))

    async def get_order(self, order_id: int) -> dict:
        order = (
            await Order.objects.select_related("client")
            .prefetch_related("items", "items__product")
            .aget(id=order_id)
        )
        order_dict = EntityOrder.model_validate(order).model_dump()
        order_dict["items"] = [
            {
                "name": p.product.name,
                "price_at_purchase": p.price_at_purchase,
                "quantity": p.quantity,
            }
            async for p in order.items.all()
        ]
        return order_dict
