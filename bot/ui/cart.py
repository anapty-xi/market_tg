from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CartItemCallback(CallbackData, prefix="cart_item"):
    index: int
    prod_id: int
    action: str = "view"


async def get_cart_kb(prod_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="🛒 Изменить корзину",
            callback_data=CartItemCallback(
                index=0, prod_id=prod_id, action="view"
            ).pack(),
        )
    )

    builder.row(
        types.InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")
    )

    return builder.as_markup()


async def get_cart_item_kb(prod_id: int, index: int, total_count: int):
    builder = InlineKeyboardBuilder()

    nav_row = []

    if index > 0:
        nav_row.append(
            types.InlineKeyboardButton(
                text="⬅️",
                callback_data=CartItemCallback(
                    index=index - 1, prod_id=prod_id, action="view"
                ).pack(),
            )
        )

    nav_row.append(
        types.InlineKeyboardButton(
            text=f"{index + 1} / {total_count}", callback_data="ignore"
        )
    )

    if index < total_count - 1:
        nav_row.append(
            types.InlineKeyboardButton(
                text="➡️",
                callback_data=CartItemCallback(
                    index=index + 1, prod_id=prod_id, action="view"
                ).pack(),
            )
        )

    builder.row(*nav_row)

    nav_row = []

    nav_row.append(
        types.InlineKeyboardButton(
            text="➕",
            callback_data=CartItemCallback(
                index=index, prod_id=prod_id, action="inc"
            ).pack(),
        )
    )
    nav_row.append(
        types.InlineKeyboardButton(
            text="➖",
            callback_data=CartItemCallback(
                index=index, prod_id=prod_id, action="dec"
            ).pack(),
        )
    )
    nav_row.append(
        types.InlineKeyboardButton(
            text="❌",
            callback_data=CartItemCallback(
                index=index, prod_id=prod_id, action="del"
            ).pack(),
        )
    )
    builder.row(*nav_row)

    builder.row(types.InlineKeyboardButton(text="🛒 В корзину", callback_data="cart"))

    return builder.as_markup()


async def get_empty_cart_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text="🛒 Вернуться к каталогу", callback_data="cart")
    )
