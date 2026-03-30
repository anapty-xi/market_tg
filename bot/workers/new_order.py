import asyncio
import json

import httpx
from aiogram import Bot
from redis.asyncio import Redis
from ui.admin import get_order_kb
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")


async def redis_order_worker(bot: Bot):
    r = Redis(
        host="redis",
        port=6379,
        db=0,
        password=secret_reader("REDIS_PASSWORD"),
        decode_responses=True,
    )

    while True:
        try:
            result = await r.brpop("order_notifications", timeout=0)

            if result:
                _, payload_json = result
                order_data = json.loads(payload_json)

                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{backend_url}/admin_group_id/")
                    group_id = response.json()["admin_group_id"]

                items_text = "\n".join(
                    [
                        f"▫️ {item['name']} — {item['quantity']} шт."
                        for item in order_data["items"]
                    ]
                )

                message_text = (
                    f"📦 Новый заказ №{order_data['order_id']}\n"
                    f"📊 Статус: {order_data['status']}\n"
                    f"👤 Клиент: {order_data['client_name']}\n"
                    f"📍 Адрес: {order_data['address']}\n\n"
                    f"🛒 Товары:\n{items_text}"
                )

                await bot.send_message(
                    chat_id=group_id,
                    text=message_text,
                    parse_mode="Markdown",
                    reply_markup=await get_order_kb(order_data["order_id"]),
                )
        except Exception:
            await asyncio.sleep(4)
