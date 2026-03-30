from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from util.secret_reader import secret_reader


class CategoryCallback(CallbackData, prefix="cat"):
    category_id: int
    action: str = "view"


class CartCallback(CallbackData, prefix="cart"):
    product_id: int
    action: str = "add"


WEB_APP_URL = secret_reader("WEB_APP_URL")


async def get_main_categories_kb(categories_list: list):
    builder = InlineKeyboardBuilder()

    builder.button(text="🛍 Открыть Магазин", web_app=WebAppInfo(url=WEB_APP_URL))

    for cat in categories_list:
        builder.button(
            text=cat["name"],
            callback_data=CategoryCallback(category_id=cat["id"], action="view"),
        )

    builder.adjust(1, 2)

    return builder.as_markup()


async def get_sub_categories_kb(subcategories_list: list):
    builder = InlineKeyboardBuilder()

    for sub in subcategories_list:
        builder.button(
            text=sub["name"],
            callback_data=CategoryCallback(category_id=sub["id"], action="products"),
        )

    builder.adjust(2)

    builder.row(
        types.InlineKeyboardButton(
            text="⬅️ Назад к категориям", callback_data="back_to_categories"
        )
    )

    return builder.as_markup()


class ProductCallback(CallbackData, prefix="prod"):
    sub_id: int
    index: int


async def get_product_kb(sub_id: int, prod_id: int, index: int, total_count: int):
    builder = InlineKeyboardBuilder()
    nav_row = []

    if index > 0:
        nav_row.append(
            types.InlineKeyboardButton(
                text="⬅️",
                callback_data=ProductCallback(sub_id=sub_id, index=index - 1).pack(),
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
                callback_data=ProductCallback(sub_id=sub_id, index=index + 1).pack(),
            )
        )

    builder.row(*nav_row)

    builder.row(
        types.InlineKeyboardButton(
            text="🛒 В корзину",
            callback_data=CartCallback(product_id=prod_id, action="add").pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📁 К категориям", callback_data="back_to_categories"
        )
    )

    return builder.as_markup()


async def get_product_dl_kb(prod_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="🛒 В корзину",
            callback_data=CartCallback(product_id=prod_id, action="add").pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📁 К категориям", callback_data="back_to_categories"
        )
    )

    return builder.as_markup()
