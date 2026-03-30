import os

import httpx
from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import BufferedInputFile, InputMediaPhoto
from loguru import logger
from ui.catalog import (
    CartCallback,
    CategoryCallback,
    ProductCallback,
    get_main_categories_kb,
    get_product_dl_kb,
    get_product_kb,
    get_sub_categories_kb,
)
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")

router = Router()


@router.message(CommandStart(deep_link=True))
async def process_start_deep_link(message: types.Message, command: CommandObject):
    args = command.args
    prod_id = int(args)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/products/0/")
        products = response.json()

    prod = None
    for p in products:
        if p["id"] == prod_id:
            prod = p
    if not prod:
        await message.answer("Неверная ссылка на товар")
        return

    relative_path = prod["images_links"][0].lstrip("/")
    file_path = os.path.join("/bot", relative_path)

    with open(file_path, "rb") as f:
        photo_bytes = f.read()

    photo = BufferedInputFile(photo_bytes, filename=os.path.basename(file_path))

    caption = f"*{prod['name']}*\n\n{prod['description']}\n\nЦена: {prod['price']}₽"

    kb = await get_product_dl_kb(prod["id"])

    await message.answer_photo(photo=photo, caption=caption, reply_markup=kb)


@router.message(Command("catalog"))
async def show_catalog(message: types.Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/main_categories/")
        categories = response.json()

    await message.answer(
        "Выберите категорию товаров:",
        reply_markup=await get_main_categories_kb(categories),
    )


@router.callback_query(CategoryCallback.filter(F.action == "view"))
async def show_subcategories(
    callback: types.CallbackQuery, callback_data: CategoryCallback
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{backend_url}/sub_categories/{callback_data.category_id}/"
        )
        subcategories = response.json()

    await callback.message.edit_text(
        text="Подкатегории:", reply_markup=await get_sub_categories_kb(subcategories)
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_categories")
async def back_to_catalog(callback: types.CallbackQuery):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/main_categories/")
        categories = response.json()

    await callback.message.delete()

    await callback.message.answer(
        text="Выберите категорию товаров:",
        reply_markup=await get_main_categories_kb(categories),
    )
    await callback.answer()


@router.callback_query(CategoryCallback.filter(F.action == "products"))
async def sub_category_click_handler(
    callback: types.CallbackQuery, callback_data: CategoryCallback
):

    await process_product_view(callback, sub_id=callback_data.category_id, index=0)


@router.callback_query(ProductCallback.filter())
async def product_pagination_handler(
    callback: types.CallbackQuery, callback_data: ProductCallback
):
    await process_product_view(
        callback, sub_id=callback_data.sub_id, index=callback_data.index
    )


async def process_product_view(callback: types.CallbackQuery, sub_id: int, index: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/products/{sub_id}/")
        products = response.json()

    if not products:
        await callback.answer("Товары не найдены", show_alert=True)
        return

    product = products[index]
    total_count = len(products)

    relative_path = product["images_links"][0].lstrip("/")
    file_path = os.path.join("/bot", relative_path)

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        await callback.answer(
            "Ошибка: Изображение товара отсутствует на сервере", show_alert=True
        )
        return

    with open(file_path, "rb") as f:
        photo_bytes = f.read()

    photo = BufferedInputFile(photo_bytes, filename=os.path.basename(file_path))

    caption = (
        f"*{product['name']}*\n\n{product['description']}\n\nЦена: {product['price']}₽"
    )

    kb = await get_product_kb(sub_id, product["id"], index, total_count)

    if callback.message.text:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=kb,
            parse_mode="Markdown",
        )
    else:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=caption, parse_mode="Markdown"),
            reply_markup=kb,
        )


@router.callback_query(CartCallback.filter(F.action == "add"))
async def add_to_cart_handler(
    callback: types.CallbackQuery, callback_data: CartCallback
):
    tg_id = callback.from_user.id
    prod_id = callback_data.product_id

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{backend_url}/cart_item/{tg_id}/?prod_id={prod_id}",
        )

    if res.status_code == 201:
        await callback.answer("Товар добавлен в корзину!", show_alert=True)
    elif res.status_code == 200:
        await callback.answer(
            "В вашей корзине уже есть этот товар, увеличили колличество на один",
            show_alert=True,
        )
