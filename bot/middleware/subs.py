from typing import Any, Awaitable, Callable, Dict

import httpx
from aiogram import BaseMiddleware, Bot
from aiogram.types import InlineKeyboardButton, TelegramObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]
        user_id = data["event_from_user"].id
        chat_id = data["event_chat"].id

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{backend_url}/admin_group_id/")
            admin_group_id = response.json()["admin_group_id"]
        if response.status_code != 200:
            return await handler(event, data)

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{backend_url}/subscription/")
            channels = response.json()

        if chat_id == admin_group_id:
            return await handler(event, data)

        not_subbed = []
        for channel in channels:
            member = await bot.get_chat_member(
                chat_id=channel["channel_id"], user_id=user_id
            )
            if member.status in ["left", "kicked"]:
                not_subbed.append(channel)

        if not_subbed:
            builder = InlineKeyboardBuilder()
            for ch in not_subbed:
                builder.row(InlineKeyboardButton(text=ch["name"], url=ch["link"]))

            if event.message:
                await event.message.answer(
                    "Чтобы пользоваться ботом, подпишитесь на наши ресурсы:",
                    reply_markup=builder.as_markup(),
                )
            elif event.callback_query:
                await event.callback_query.answer(
                    "Сначала подпишитесь!", show_alert=True
                )

            return

        return await handler(event, data)
