from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.consts import ENTERED_PARAMETERS_PATTERN, PARAMETER_NOT_SET
from src.database import AsyncBotDatabase
from src.external_service.api import ExternalScienceAPI
from src.external_service.service import get_papers_information
from src.keybords.service import (create_pagination_keyboard,
                                  get_started_keyboard,
                                  start_reading_papers_keyboard)
from src.lexicons.lexicon_rus import LEXICON_RUS

router = Router()


@router.message(F.text == LEXICON_RUS['entered_parameters'])
async def check_entered_parameters(message: Message, database: AsyncBotDatabase):
    parameters = await database.fetch_one_last_data(
        table_name='parameters',
        searching_columns=['terms', 'source_published', 'authors', 'min_years', 'max_years', 'min_pages', 'max_pages'],
        user_id=message.from_user.id
    )
    not_null_parameters = tuple(parameter if parameter else PARAMETER_NOT_SET for parameter in parameters)
    await message.answer(text=ENTERED_PARAMETERS_PATTERN % not_null_parameters)


@router.message(F.text == LEXICON_RUS['run_aggregation_papers'])
async def search_science_api(
        message: Message,
        database: AsyncBotDatabase,
        external_service: ExternalScienceAPI,
        state: FSMContext
):
    parameters = await database.fetch_one_last_data(
        table_name='parameters',
        searching_columns=['terms', 'source_published', 'authors', 'min_years', 'max_years', 'min_pages', 'max_pages'],
        user_id=message.from_user.id
    )
    print(f'{parameters=}')
    raw_science_papers_models = await external_service.get_works(*parameters)
    science_papers = get_papers_information(papers_models=raw_science_papers_models)
    await state.update_data(papers=science_papers)
    await message.answer(
        text='Найдено %d записей.\n\n'
             'Чтобы начать чтение - выберите поле на клавиатуре' % len(science_papers),
        reply_markup=start_reading_papers_keyboard()
    )


@router.message(F.text == LEXICON_RUS['read'])
async def start_reading(message: Message, database: AsyncBotDatabase, state: FSMContext):
    state_data = await state.get_data()
    papers = state_data['papers']
    page_number, total_pages = 1, len(papers) - 1
    await database.insert_data(
        table_name='page_information',
        inserted_data={'current_page': page_number, 'total_pages': total_pages},
        user_id=message.from_user.id
    )
    paper_details = papers[page_number]
    await message.answer(
        text=paper_details,
        reply_markup=create_pagination_keyboard(
            page_number=page_number,
            total_pages=total_pages
        ))


@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery, database: AsyncBotDatabase, state: FSMContext) -> None:
    state_data = await state.get_data()
    papers = state_data['papers']
    page_number, total_pages = await database.fetch_one_last_data(
        table_name='page_information',
        searching_columns=['current_page', 'total_pages'],
        user_id=callback.from_user.id
    )
    if page_number < total_pages:
        page_number += 1
        paper_details = papers[page_number]
        await database.update_data(
            table_name='page_information',
            updated_data={'current_page': page_number},
            user_id=callback.from_user.id
        )
        await callback.message.edit_text(
            text=paper_details,
            reply_markup=create_pagination_keyboard(page_number=page_number, total_pages=total_pages)
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery, database: AsyncBotDatabase, state: FSMContext) -> None:
    state_data = await state.get_data()
    papers = state_data['papers']
    page_number, total_pages = await database.fetch_one_last_data(
        table_name='page_information',
        searching_columns=['current_page', 'total_pages'],
        user_id=callback.from_user.id
    )
    if page_number > 1:
        page_number -= 1
        paper_details = papers[page_number]
        await database.update_data(
            table_name='page_information',
            updated_data={'current_page': page_number},
            user_id=callback.message.from_user.id
        )
        await callback.message.edit_text(
            text=paper_details,
            reply_markup=create_pagination_keyboard(page_number=page_number, total_pages=total_pages)
        )
    await callback.answer()


#
# # Закладки
# @router.message(Command(commands='bookmarks'))
# async def process_bookmarks_command(message: Message, database: AsyncBotDatabase):
#     bookmarks = await database.fetch_one_last_data(
#         table_name='bookmarks',
#         searching_columns=['title', 'id', 'year'],
#         user_id=message.from_user.id
#     )
#     if bookmarks:
#         ...


@router.message(F.text == LEXICON_RUS['back'])
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Возврат к основному меню', reply_markup=get_started_keyboard())
