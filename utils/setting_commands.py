from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScope, BotCommandScopeDefault, BotCommandScopeChat


async def set_starting_commands(bot: Bot, chat_id: int):
    starting_commands = {
        'ru': [
            BotCommand("start", '🤖Главное меню.'),
            BotCommand("help", '❔О боте')
        ],
        'en': [
            BotCommand("start", '🤖Main menu'),
            BotCommand("help", '❔Info')
        ]
    }
    for language_code, commands in starting_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChat(chat_id),
            language_code=language_code
        )
