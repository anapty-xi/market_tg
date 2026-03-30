from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_commands(bot: Bot, chat_id: int):
    """Устанавливает личное меню для авторизованного пользователя"""
    commands = [
        BotCommand(command="catalog", description="🛍 Каталог товаров"),
        BotCommand(command="cart", description="🛒 Корзина"),
        BotCommand(command="help", description="❓ Помощь и поддержка"),
    ]

    await bot.set_my_commands(
        commands=commands, scope=BotCommandScopeChat(chat_id=chat_id)
    )
