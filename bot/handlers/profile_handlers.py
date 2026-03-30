import httpx
from aiogram import F, Router, types
from aiogram.filters import Command
from handlers.common_handlers import set_commands
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")
router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    async with httpx.AsyncClient() as client:
        user_exists = await client.get(f"{backend_url}/profile/{tg_id}/{username}/")

    if user_exists.status_code == 200:
        await set_commands(message.bot, chat_id=tg_id)
        await message.answer(f"С возвращением, {message.from_user.first_name}!")
    else:
        contact_button = [
            [types.KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=contact_button, resize_keyboard=True
        )
        await set_commands(message.bot, chat_id=tg_id)
        await message.answer(
            "Добро пожаловать! Чтобы делать покупки, нам нужен ваш номер телефона.",
            reply_markup=keyboard,
        )


@router.message(F.contact)
async def get_contact(message: types.Message):
    phone = message.contact.phone_number
    tg_id = message.from_user.id
    username = message.from_user.username

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{backend_url}/profile/",
            json={"tg_id": tg_id, "username": username, "phone_number": phone},
        )

    if res.status_code == 201:
        await message.answer(
            "Регистрация завершена! Теперь вы можете перейти в магазин.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
