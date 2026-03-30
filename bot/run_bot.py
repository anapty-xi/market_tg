import asyncio

from aiogram import Bot, Dispatcher
from handlers import (
    admin_handlers,
    cart_handlers,
    catalog_handlers,
    order_handlers,
    profile_handlers,
)
from loguru import logger
from middleware.subs import CheckSubscriptionMiddleware
from util.secret_reader import secret_reader
from workers import new_order, status_change

BOT_TOKEN = secret_reader("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.update.outer_middleware(CheckSubscriptionMiddleware())
    dp.include_router(catalog_handlers.router)
    dp.include_router(cart_handlers.router)
    dp.include_router(profile_handlers.router)

    dp.include_router(order_handlers.router)

    dp.include_router(admin_handlers.router)

    new_order_admin_note = asyncio.create_task(new_order.redis_order_worker(bot))
    status_change_task_note = asyncio.create_task(status_change.status_change(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.success("server up and running")
    asyncio.run(main())
