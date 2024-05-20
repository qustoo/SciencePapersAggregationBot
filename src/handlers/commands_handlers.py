from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove

from src.consts import HELP_MESSAGE, START_MESSAGE
from src.keybords.service import (get_searching_parameters_keyboard,
                                  get_started_keyboard)
from src.lexicons.lexicon_rus import LEXICON_RUS

user_router = Router()


# /start
@user_router.message(F.text == '/start')
async def start_command(message: Message):
    await message.answer(text=START_MESSAGE, reply_markup=get_started_keyboard())


# /help
@user_router.message(F.text == LEXICON_RUS['help'])
async def help_command(message: Message):
    await message.answer(text=HELP_MESSAGE)


# base searching
@user_router.message(F.text.in_({
    LEXICON_RUS['start_fill_based_parameters'],
    LEXICON_RUS['back_to_based_searching_keyboard']})
)
async def base_searching(message: Message):
    await message.answer(
        text='Начинаем!',
        reply_markup=get_searching_parameters_keyboard()
    )


# fill advanced parameters


# cancel searching
@user_router.message(F.text == LEXICON_RUS['cancel'])
async def cancel_searching(message: Message):
    await message.reply(text='Может в другой раз)', reply_markup=ReplyKeyboardRemove())
