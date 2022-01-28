from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked

from utils.db_commands import Users


async def broadcast(bot: Bot, broadcast_text: str, markup: (ReplyKeyboardMarkup, InlineKeyboardMarkup) = None,
                    photo: str = None):
    users = await Users.get_all()
    if not photo:
        for user in users:
            try:
                await bot.send_message(user[0], broadcast_text, reply_markup=markup)
            except BotBlocked:
                continue
    else:
        async with open(photo) as file:
            data = file.read()
        for user in users:
            try:
                await bot.send_photo(user[0], photo=data, caption=broadcast_text, reply_markup=markup)
            except BotBlocked:
                continue
