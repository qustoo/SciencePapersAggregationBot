from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from src.database import AsyncBotDatabase
from src.keybords.service import (create_bookmarks_keyboard,
                                  get_searching_parameters_keyboard,
                                  get_started_keyboard)
from src.lexicons.lexicon_rus import LEXICON_COMMANDS_RU, LEXICON_RUS

router = Router()


@router.message(Command(commands='start'))
async def start_command(message: Message):
    await message.answer(text=LEXICON_COMMANDS_RU['/start'], reply_markup=get_started_keyboard())


@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(text=LEXICON_COMMANDS_RU['/help'])


@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message, database: AsyncBotDatabase):
    bookmarks = await database.fetch_user_bookmarks_data(user_id=message.from_user.id)
    if bookmarks:
        await message.answer(
            text='Найденные заметки:\n\n',
            reply_markup=create_bookmarks_keyboard(*bookmarks)
        )
    else:
        await message.answer(text=LEXICON_RUS['no_bookmarks'])


@router.message(F.text == LEXICON_RUS['start_fill_based_parameters'])
async def base_searching(message: Message):
    await message.answer(
        text='Начинаем!',
        reply_markup=get_searching_parameters_keyboard()
    )


# cancel searching
@router.message(F.text == LEXICON_RUS['cancel'])
async def cancel_searching(message: Message):
    await message.reply(text=' ', reply_markup=ReplyKeyboardRemove())
