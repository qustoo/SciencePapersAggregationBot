import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, FILENAME_DATABASE
from consts import LOGGING_FORMAT
from database import db
from handlers import (commands_handlers, error_handlers, parameters_handlers,
                      science_api_handlers)
from src.keybords.main_menu import set_main_menu
from src.middlewares.additional_services_middleware import DataBaseMiddleware

logger = logging.getLogger(__name__)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

dp.update.middleware(DataBaseMiddleware(FILENAME_DATABASE))

dp.include_router(commands_handlers.router)
dp.include_router(parameters_handlers.router)
dp.include_router(science_api_handlers.router)
dp.include_router(error_handlers.router)


async def main():
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
    logger.info('Starting bot')
    await set_main_menu(bot)
    dp.startup.register(callback=db.create_tables)
    dp.shutdown.register(callback=db.drop_tables)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
