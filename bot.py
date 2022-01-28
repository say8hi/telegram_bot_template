import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from config import load_config
from filters.role import RoleFilter, AdminFilter
from handlers.error_handler import register_errors
from handlers.general import register_user
from middlewares.role import RoleMiddleware

logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher):
    register_user(dp)
    register_errors(dp)


async def main():
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logger.info("Starting bot")
    config = load_config()

    storage = RedisStorage() if config.tg_bot.use_redis else MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admins))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped!")
