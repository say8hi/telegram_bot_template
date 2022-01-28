from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, Message

from filters.all_filters import IsPrivate
from utils.db_commands import Users
from utils.setting_commands import set_starting_commands


async def close_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()


async def bot_start(message: Message, state: FSMContext):
    await state.finish()
    user = await Users.get(message.from_user.id, message.from_user.username)
    await set_starting_commands(message.bot, message.from_user.id)
    await message.answer(f"<b>Welcome, <pre>{user.username}</></b>")


# async def test(message: Message, state: FSMContext):
#     await message.reply("good")


def register_user(dp: Dispatcher):
    dp.register_callback_query_handler(close_handler, text="close", state="*")
    dp.register_message_handler(bot_start, IsPrivate(), CommandStart(), state="*")
    # dp.register_message_handler(test, commands=['test'], state="*")
