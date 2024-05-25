from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database import AsyncBotDatabase
from src.keybords.service import (create_bookmarks_keyboard,
                                  get_started_keyboard,
                                  start_reading_own_papers_keyboard)
from src.lexicons.lexicon_rus import LEXICON_COMMANDS_DESCRIPTION, LEXICON_RUS
from src.utils.external_services_utils import get_papers_representation

router = Router()


@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_COMMANDS_DESCRIPTION['/start'],
        parse_mode=ParseMode.HTML,
        reply_markup=get_started_keyboard()
    )


@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message, database: AsyncBotDatabase):
    bookmarks = await database.fetch_user_bookmarks_data(user_id=message.from_user.id)
    if bookmarks:
        await message.answer(
            text=LEXICON_RUS['bookmarks'],
            reply_markup=create_bookmarks_keyboard(*bookmarks)
        )
    else:
        await message.answer(text=LEXICON_RUS['no_bookmarks'])


@router.message(F.text == LEXICON_RUS['help'])
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_COMMANDS_DESCRIPTION['/help'])


@router.message(Command(commands='my_papers'))
async def process_papers_commands(message: Message, database: AsyncBotDatabase, state: FSMContext):
    user_papers = await database.fetch_data(
        table_name='papers',
        searching_columns=[
            'link', 'doi', 'title', 'abstract', 'publication_date', 'cites', 'topic', 'authors', 'sources'],
        filter_columns={'user_id': message.from_user.id},
        fetchall=True
    )

    if user_papers:
        unique_papers = list(set(user_papers))
        science_papers_representation = get_papers_representation(unique_papers)
        await state.update_data(papers_data=science_papers_representation)
        await message.answer(
            text=f'Найдено {len(science_papers_representation)} ранее найденых вами статей.\n\n'
                 'Чтобы начать чтение - выберите поле на клавиатуре',
            reply_markup=start_reading_own_papers_keyboard()
        )

    else:
        await message.answer(
            text='Не найдено обнаруженых ваши статей в базе данных.\n\n',
            reply_markup=get_started_keyboard()
        )


@router.message(F.text == LEXICON_RUS['cancel'])
async def process_cancel_searching(message: Message):
    await message.answer(text=LEXICON_RUS['cancel_message'] + '\n\n', reply_markup=get_started_keyboard())
