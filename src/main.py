import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, FILENAME_DATABASE
from consts import LOGGING_FORMAT
from handlers import commands_handlers, science_api_handlers, states_handlers
from src.middlewares.additional_services_middleware import DataBaseMiddleware

logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

dp.update.middleware(DataBaseMiddleware(FILENAME_DATABASE))

dp.include_router(commands_handlers.router)
dp.include_router(states_handlers.router)
dp.include_router(science_api_handlers.router)


async def main():
    # dp.startup.register(callback=db.create_table)
    # dp.shutdown.register(callback=db.drop_table)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
