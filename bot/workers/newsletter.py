import asyncio
import os

import httpx
from aiogram import Bot
from aiogram.types import BufferedInputFile
from celery import Celery
from util.secret_reader import secret_reader

app = Celery(
    "newsletter_tasks",
    broker=f"redis://:{secret_reader('REDIS_PASSWORD')}@redis:6379/0",
)

bot = Bot(token=secret_reader("BOT_TOKEN"))


@app.task(name="execute_newsletter_mailing")
def execute_newsletter_mailing(payload):
    async def run_broadcast():
        text = payload.get("text")
        image_path = payload.get("image").lstrip("/") if payload.get("image") else None

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{secret_reader('API_URL')}/users/")
            users = response.json()

        for u in users:
            try:
                if image_path:
                    file_path = os.path.join("/bot", image_path)

                    with open(file_path, "rb") as f:
                        photo_bytes = f.read()

                    photo = BufferedInputFile(
                        photo_bytes, filename=os.path.basename(file_path)
                    )

                    await bot.send_photo(
                        chat_id=u["tg_id"],
                        photo=photo,
                        caption=text,
                        parse_mode="Markdown",
                    )

                else:
                    await bot.send_message(
                        chat_id=u["tg_id"], text=text, parse_mode="Markdown"
                    )
                await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Не удалось отправить сообщение {u['tg_id']}: {e}")

        await bot.session.close()

    asyncio.run(run_broadcast())
