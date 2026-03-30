import httpx
from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from ui.admin import OrderCallback, get_order_kb, get_order_text, get_status_change_kb
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")

router = Router()


@router.message(Command("active"))
async def get_active_orders(message: types.Message, bot: Bot):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/admin_group_id/")
        group_id = response.json()["admin_group_id"]

    if message.chat.id != group_id:
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/active_orders/")
        orders = response.json()

    for order in orders:
        await message.answer(
            text=await get_order_text(
                order["items"],
                order["id"],
                order["status"],
                order["client_full_name"],
                order["address"],
            ),
            reply_markup=await get_order_kb(order["id"]),
        )


@router.callback_query(OrderCallback.filter(F.action == "change_status"))
async def change_order_status_handler(
    callback: types.CallbackQuery, callback_data: OrderCallback
):
    await callback.message.edit_reply_markup(
        reply_markup=await get_status_change_kb(callback_data.order_id)
    )


@router.callback_query(OrderCallback.filter(F.action == "set_paid"))
async def set_paid_handler(callback: types.CallbackQuery, callback_data: OrderCallback):
    async with httpx.AsyncClient() as client:
        await client.patch(f"{backend_url}/order/{callback_data.order_id}/?status=paid")
    await callback.answer("Статус заказа изменён на 'Оплачен'.", show_alert=True)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/order/{callback_data.order_id}/")
        order = response.json()

    await callback.message.edit_text(
        text=await get_order_text(
            order["items"],
            callback_data.order_id,
            order["status"],
            order["client_full_name"],
            order["address"],
        ),
        reply_markup=await get_order_kb(callback_data.order_id),
    )


@router.callback_query(OrderCallback.filter(F.action == "set_unpaid"))
async def set_unpaid_handler(
    callback: types.CallbackQuery, callback_data: OrderCallback
):
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{backend_url}/order/{callback_data.order_id}/?status=unpaid"
        )
    await callback.answer("Статус заказа изменён на 'Не оплачен'.", show_alert=True)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/order/{callback_data.order_id}/")
        order = response.json()

    await callback.message.edit_text(
        text=await get_order_text(
            order["items"],
            callback_data.order_id,
            order["status"],
            order["client_full_name"],
            order["address"],
        ),
        reply_markup=await get_order_kb(callback_data.order_id),
    )


@router.callback_query(OrderCallback.filter(F.action == "set_in_transit"))
async def set_in_transiton_handler(
    callback: types.CallbackQuery, callback_data: OrderCallback
):
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{backend_url}/order/{callback_data.order_id}/?status=on_the_way"
        )
    await callback.answer("Статус заказа изменён на 'В пути'.", show_alert=True)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/order/{callback_data.order_id}/")
        order = response.json()

    await callback.message.edit_text(
        text=await get_order_text(
            order["items"],
            callback_data.order_id,
            order["status"],
            order["client_full_name"],
            order["address"],
        ),
        reply_markup=await get_order_kb(callback_data.order_id),
    )


@router.callback_query(OrderCallback.filter(F.action == "set_completed"))
async def set_completed_handler(
    callback: types.CallbackQuery, callback_data: OrderCallback
):
    async with httpx.AsyncClient() as client:
        await client.patch(f"{backend_url}/order/{callback_data.order_id}/?status=done")

    await callback.answer("Статус заказа изменён на 'Завершён'.", show_alert=True)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{backend_url}/order/{callback_data.order_id}/")
        order = response.json()

    await callback.message.edit_text(
        text=await get_order_text(
            order["items"],
            callback_data.order_id,
            order["status"],
            order["client_full_name"],
            order["address"],
        ),
        reply_markup=await get_order_kb(callback_data.order_id),
    )
