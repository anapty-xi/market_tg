import httpx
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from states.order_states import CheckoutOrder
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")

router = Router()


@router.callback_query(F.data == "checkout")
async def start_checkout(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(
        "Пожалуйста, введите данные для заказа, следую инструкциям", show_alert=True
    )
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(CheckoutOrder.waiting_for_name)


@router.message(CheckoutOrder.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите адрес доставки:")
    await state.set_state(CheckoutOrder.waiting_for_address)


@router.message(CheckoutOrder.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)

    payment_url = "https://github.com/anapty-xi"  # Здесь должна быть логика генерации ссылки на оплату

    data = await state.get_data()
    text = f"Ваши данные:\nИмя: {data.get('name')}\n\nАдрес: {data.get('address')}\n\nПожалуйста, оплатите заказ по ссылке ниже.\n\n"

    builder = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="💳 Оплатить\n", url=payment_url)],
            [
                types.InlineKeyboardButton(
                    text="✅ Я оплатил", callback_data="confirm_payment"
                )
            ],
        ]
    )

    await message.answer(
        text,
        reply_markup=builder,
    )
    await state.set_state(CheckoutOrder.waiting_for_payment)


@router.callback_query(CheckoutOrder.waiting_for_payment, F.data == "confirm_payment")
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    address = user_data.get("address")

    async with httpx.AsyncClient() as client:
        await client.post(
            f"{backend_url}/order/",
            json={
                "tg_id": callback.from_user.id,
                "client_full_name": name,
                "address": address,
            },
        )

    await callback.message.edit_text(f"Спасибо, {name}! Заказ оформлен.")
