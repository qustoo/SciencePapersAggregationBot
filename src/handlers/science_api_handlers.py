from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.consts import ENTERED_PARAMETERS_PATTERN, PARAMETER_NOT_SET
from src.database import AsyncBotDatabase
from src.external_service.api import ExternalScienceAPI
from src.filters.bookmarks_filters import IsDelBookmarkCallbackData
from src.keybords.service import (create_edit_keyboard,
                                  create_pagination_keyboard,
                                  get_started_keyboard,
                                  start_reading_papers_keyboard)
from src.lexicons.lexicon_rus import LEXICON_RUS
from src.utils.external_services_utils import get_papers_representation
from src.utils.papers_utils import add_papers_to_database

router = Router()


@router.message(F.text == LEXICON_RUS['entered_parameters'])
async def check_entered_parameters(message: Message, database: AsyncBotDatabase):
    parameters = await database.fetch_data(
        table_name='parameters',
        searching_columns=['terms', 'source_published', 'authors', 'min_years', 'max_years', 'min_pages', 'max_pages'],
        filter_columns={'user_id': message.from_user.id},
        fetchone=True,
    )
    if parameters:
        not_null_parameters = tuple(parameter if parameter else PARAMETER_NOT_SET for parameter in parameters)
        await message.answer(text=ENTERED_PARAMETERS_PATTERN % not_null_parameters)
    else:
        await message.answer(text=LEXICON_RUS['no_one_saved_parameters'])


@router.message(F.text == LEXICON_RUS['run_aggregation_papers'])
async def search_science_api(
        message: Message,
        database: AsyncBotDatabase,
        external_service: ExternalScienceAPI,
        state: FSMContext,
):
    parameters = await database.fetch_data(
        table_name='parameters',
        searching_columns=['terms', 'source_published', 'authors', 'min_years', 'max_years', 'min_pages', 'max_pages'],
        filter_columns={'user_id': message.from_user.id},
        fetchone=True
    )
    if parameters:
        raw_science_papers = await external_service.get_works(*parameters)
        await add_papers_to_database(papers=raw_science_papers, database=database, user_id=message.from_user.id)
        represented_science_papers = get_papers_representation(raw_science_papers)

        await state.update_data(papers_data=represented_science_papers)
        await message.answer(
            text=f'Найдено {len(raw_science_papers)} записей.\n\n'
                 'Чтобы начать чтение - выберите поле на клавиатуре',
            reply_markup=start_reading_papers_keyboard()
        )
    else:
        await message.answer(
            text='Не обнаружено параметров данных для поиска статей.\n\n Пожалуйста, введите их, выбрав поле в меню,'
                 'и проверьте что они сохранены.\n\n'
        )


@router.message(F.text == LEXICON_RUS['read'])
async def process_start_reading(message: Message, database: AsyncBotDatabase, state: FSMContext):
    state_data = await state.get_data()
    papers_data = state_data['papers_data']
    page_number, total_pages = 1, len(papers_data) - 1

    paper = papers_data[page_number]
    paper_representation, paper_link = paper.representation, paper.link

    await state.update_data(paper_link=paper_link)

    await database.insert_data(
        table_name='page_information',
        inserted_data={'current_page': page_number, 'total_pages': total_pages},
        user_id=message.from_user.id
    )

    await message.answer(
        text=paper_representation,
        reply_markup=create_pagination_keyboard(
            page_number=page_number,
            total_pages=total_pages
        ))


@router.callback_query(F.data.in_({'forward', 'backward'}))
async def process_forward_backward_press(callback: CallbackQuery, database: AsyncBotDatabase, state: FSMContext):
    state_data = await state.get_data()
    papers_data = state_data['papers_data']
    page_number, total_pages = await database.fetch_data(
        table_name='page_information',
        searching_columns=['current_page', 'total_pages'],
        filter_columns={'user_id': callback.from_user.id},
        fetchone=True,
    )
    if callback.data == 'forward':
        page_number += 1
    elif callback.data == 'backward':
        page_number -= 1

    paper = papers_data[page_number]
    paper_representation, paper_link = paper.representation, paper.link

    await state.update_data(paper_link=paper_link)
    await database.update_data(
        table_name='page_information',
        updated_data={'current_page': page_number},
        user_id=callback.from_user.id
    )

    await callback.message.edit_text(
        text=paper_representation,
        reply_markup=create_pagination_keyboard(page_number=page_number, total_pages=total_pages)
    )


@router.callback_query(F.data == 'add_to_bookmarks')
async def add_current_paper_to_bookmarks(callback: CallbackQuery, database: AsyncBotDatabase, state: FSMContext):
    state_data = await state.get_data()
    paper_link = state_data['paper_link']

    paper_id_data = await database.fetch_data(
        table_name='papers',
        searching_columns=['id'],
        filter_columns={'link': paper_link, 'user_id': callback.from_user.id},
        fetchone=True

    )
    paper_id = paper_id_data[0]

    await database.insert_data(
        table_name='bookmarks',
        inserted_data={'paper_id': paper_id},
        user_id=callback.from_user.id
    )
    await callback.answer(text='Статья добавлена в закладки!\n\n')


@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery, database: AsyncBotDatabase):
    bookmarks = await database.fetch_user_bookmarks_data(user_id=callback.from_user.id)
    await callback.message.edit_text(
        text='Найденные закладки:\n\n',
        reply_markup=create_edit_keyboard(
            *bookmarks
        ))


@router.callback_query(F.data == 'cancel_bookmarks')
async def process_cancel_show_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RUS['cancel_editing_bookmarks']
    )


@router.callback_query(IsDelBookmarkCallbackData())
async def delete_bookmark(callback: CallbackQuery, paper_link: str, database: AsyncBotDatabase):
    paper_id_data = await database.fetch_data(
        table_name='papers',
        searching_columns=['id'],
        filter_columns={'link': paper_link, 'user_id': callback.from_user.id},
        fetchone=True
    )
    paper_id = paper_id_data[0]
    await database.remove_data(
        table_name='bookmarks',
        removed_data={'paper_id': paper_id, 'user_id': callback.from_user.id}
    )
    await process_edit_press(callback=callback, database=database)


@router.message(F.text == LEXICON_RUS['read_own_papers'])
async def process_read_own_papers(message: Message, database: AsyncBotDatabase, state: FSMContext):
    state_data = await state.get_data()
    papers_data = state_data['papers_data']
    page_number, total_pages = 1, len(papers_data) - 1

    paper = papers_data[page_number]
    paper_representation, paper_link = paper.representation, paper.link

    await state.update_data(paper_link=paper_link)

    await database.insert_data(
        table_name='page_information',
        inserted_data={'current_page': page_number, 'total_pages': total_pages},
        user_id=message.from_user.id
    )

    await message.answer(
        text=paper_representation,
        reply_markup=create_pagination_keyboard(
            page_number=page_number,
            total_pages=total_pages
        ))


@router.message(F.text == LEXICON_RUS['back'])
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Возврат к основному меню', reply_markup=get_started_keyboard())
