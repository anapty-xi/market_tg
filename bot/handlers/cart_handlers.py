from decimal import Decimal

import httpx
from aiogram import F, Router, types
from aiogram.filters import Command
from ui.cart import CartItemCallback, get_cart_item_kb, get_cart_kb, get_empty_cart_kb
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")

router = Router()


@router.message(Command("cart"))
async def show_cart(message: types.Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{message.from_user.id}/")
        cart_items = response.json()

    if response.status_code != 200 or not cart_items:
        await message.answer("Ваша корзина пуста.")
        return
    else:
        text = "Ваша корзина:\n\n"
        total = 0

        for index, item in enumerate(cart_items):
            text += f"{index + 1}. {item['product']['name']} - {item['quantity']} шт. - {item['total_price']} руб.\n\n"
            total += Decimal(item["total_price"])

        text += f"Итого: {total} руб."

        await message.answer(
            text, reply_markup=await get_cart_kb(item["product"]["id"])
        )


@router.callback_query(F.data == "cart")
async def show_cart_callback(callback: types.CallbackQuery):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{callback.from_user.id}/")
        cart_items = sorted(response.json(), key=lambda item: item["id"])

        text = "Ваша корзина:\n\n"
        total = 0

        for index, item in enumerate(cart_items):
            text += f"{index + 1}. {item['product']['name']} - {item['quantity']} шт. - {item['total_price']} руб.\n\n"
            total += Decimal(item["total_price"])

        text += f"Итого: {total} руб."

        await callback.message.edit_text(
            text, reply_markup=await get_cart_kb(item["product"]["id"])
        )


@router.callback_query(CartItemCallback.filter(F.action == "view"))
async def cart_items_list_handler(
    callback: types.CallbackQuery, callback_data: CartItemCallback
):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{callback.from_user.id}/")
        cart_items = sorted(response.json(), key=lambda item: item["id"])

    if response.status_code != 200 or not cart_items:
        await callback.message.edit_text(
            "Ваша корзина пуста.", reply_markup=await get_empty_cart_kb()
        )
        return

    item = cart_items[callback_data.index]
    text = f"{item['product']['name']} - {item['quantity']} шт. - {item['total_price']} руб."

    await callback.message.edit_text(
        text,
        reply_markup=await get_cart_item_kb(
            cart_items[callback_data.index]["product"]["id"],
            callback_data.index,
            len(cart_items),
        ),
    )


@router.callback_query(CartItemCallback.filter(F.action == "inc"))
async def increase_item_quantity(
    callback: types.CallbackQuery, callback_data: CartItemCallback
):
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{backend_url}/cart_item/{callback.from_user.id}/?prod_id={callback_data.prod_id}&increase=True",
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{callback.from_user.id}/")
        cart_items = sorted(response.json(), key=lambda item: item["id"])

    item = cart_items[callback_data.index]
    text = f"{item['product']['name']} - {item['quantity']} шт. - {item['total_price']} руб."

    await callback.message.edit_text(
        text,
        reply_markup=await get_cart_item_kb(
            item["product"]["id"],
            callback_data.index,
            len(cart_items),
        ),
    )


@router.callback_query(CartItemCallback.filter(F.action == "dec"))
async def decrease_item_quantity(
    callback: types.CallbackQuery, callback_data: CartItemCallback
):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{callback.from_user.id}/")
        cart_items = sorted(response.json(), key=lambda item: item["id"])

    if cart_items[callback_data.index]["quantity"] == 1:
        await callback.answer(
            "Невозможно уменьшить количество товара. Для удаления товара из корзины нажмите кнопку ❌",
            show_alert=True,
        )
        return

    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{backend_url}/cart_item/{callback.from_user.id}/?prod_id={callback_data.prod_id}&increase=False",
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{callback.from_user.id}/")
        cart_items = sorted(response.json(), key=lambda item: item["id"])

    if response.status_code != 200:
        await callback.message.edit_text(
            "Ваша корзина пуста.", reply_markup=await get_empty_cart_kb()
        )
        return

    item = cart_items[callback_data.index]
    text = f"{item['product']['name']} - {item['quantity']} шт. - {item['total_price']} руб."

    await callback.message.edit_text(
        text,
        reply_markup=await get_cart_item_kb(
            item["product"]["id"], callback_data.index, len(cart_items)
        ),
    )


@router.callback_query(CartItemCallback.filter(F.action == "del"))
async def delete_item_from_cart(
    callback: types.CallbackQuery, callback_data: CartItemCallback
):
    async with httpx.AsyncClient() as client:
        await client.delete(
            f"{backend_url}/cart_item/{callback.from_user.id}/?prod_id={callback_data.prod_id}",
        )
    await callback.answer("Товар удален из корзины!", alert=True)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/cart/{callback.from_user.id}/")
        cart_items = sorted(response.json(), key=lambda item: item["id"])

    if response.status_code != 200 or not cart_items:
        await callback.message.edit_text(
            "Ваша корзина пуста.", reply_markup=await get_empty_cart_kb()
        )
        return

    item = cart_items[0]
    text = f"{item['product']['name']} - {item['quantity']} шт. - {item['total_price']} руб."

    await callback.message.edit_text(
        text,
        reply_markup=await get_cart_item_kb(item["product"]["id"], 0, len(cart_items)),
    )
