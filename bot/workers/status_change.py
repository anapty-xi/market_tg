import asyncio
import json

from aiogram import Bot
from loguru import logger
from redis.asyncio import Redis
from util.secret_reader import secret_reader

backend_url = secret_reader("API_URL")


async def status_change(bot: Bot):
    r = Redis(
        host="redis",
        port=6379,
        db=0,
        password=secret_reader("REDIS_PASSWORD"),
        decode_responses=True,
    )
    logger.info("Status change worker started")

    while True:
        try:
            result = await r.brpop("order_status_changed", timeout=0)
            logger.info("Received status change notification: {}", result)

            if result:
                _, payload_json = result
                order_data = json.loads(payload_json)

                text = f"Ваш заказ {order_data['order_id']} изменил статус на {order_data['new_status']}\n"

                await bot.send_message(
                    chat_id=order_data["tg_id"],
                    text=text,
                    parse_mode="Markdown",
                )
        except Exception as e:
            logger.error("Error occurred while handling status change: {}", e)
            await asyncio.sleep(4)
