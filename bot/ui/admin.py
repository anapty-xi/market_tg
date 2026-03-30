from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class OrderCallback(CallbackData, prefix="order"):
    order_id: int
    action: str = "change_status"


async def get_order_kb(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="📑 Изменить статус",
            callback_data=OrderCallback(
                order_id=order_id, action="change_status"
            ).pack(),
        )
    )
    return builder.as_markup()


async def get_status_change_kb(order_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="❌Неоплачен",
            callback_data=OrderCallback(order_id=order_id, action="set_unpaid").pack(),
        ),
        types.InlineKeyboardButton(
            text="💸 Оплачен",
            callback_data=OrderCallback(order_id=order_id, action="set_paid").pack(),
        ),
    )

    builder.row(
        types.InlineKeyboardButton(
            text="✈️ В пути",
            callback_data=OrderCallback(
                order_id=order_id, action="set_in_transit"
            ).pack(),
        ),
        types.InlineKeyboardButton(
            text="✅ Выполнен",
            callback_data=OrderCallback(
                order_id=order_id, action="set_completed"
            ).pack(),
        ),
    )

    return builder.as_markup()


async def get_order_text(
    items: list, order_id: int, status: str, client_full_name, address
):
    items_text = "\n".join(
        [f"▫️ {item['name']} — {item['quantity']} шт." for item in items]
    )

    message_text = (
        f"📦 Новый заказ №{order_id}\n"
        f"📊 Статус: {status}\n"
        f"👤 Клиент: {client_full_name}\n"
        f"📍 Адрес: {address}\n\n"
        f"🛒 Товары:\n{items_text}"
    )

    return message_text
