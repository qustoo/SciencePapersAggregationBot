import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from consts import LOGGING_FORMAT
from handlers import commands_handlers, states_handlers, check_entered_parameters_handlers, external_api_handlers
from database import db

logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

dp.include_router(commands_handlers.user_router)
dp.include_router(states_handlers.searching_states_router)
dp.include_router(check_entered_parameters_handlers.entered_parameters_router)
dp.include_router(external_api_handlers.external_science_router)


# dp.include_router(science_api_router)

# # another messages
# @dp.message()
# async def incorrect_command(message: Message):
#     await message.reply(text='Неверная команда!')


async def main():
    dp.startup.register(callback=db.create_table)
    dp.shutdown.register(callback=db.drop_table)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
