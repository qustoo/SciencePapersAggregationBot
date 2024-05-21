from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from src.database import AsyncBotDatabase
from src.filters.searching_parameters_filters import (
    PagesSearchingParametersFilters, TextSearchingParametersFilters,
    YearsSearchingParametersFilters)
from src.keybords.service import (finished_entering_parameters_keyboards,
                                  get_searching_parameters_keyboard,
                                  get_started_keyboard)
from src.lexicons.lexicon_rus import LEXICON_RUS
from src.states.papers_parameters_states import \
    ScienceSearchingParametersStates
from src.utils.states_enums import StatesName
from src.utils.states_utils import (update_state_data,
                                    upload_data_and_reset_state)

router = Router()


# terms
@router.message(StateFilter(default_state), F.text == LEXICON_RUS['terms'])
async def process_terms_parameters(message: Message, state: FSMContext):
    await message.answer(
        text='Введите ключевые слова(machine learning): ',
        reply_markup=finished_entering_parameters_keyboards()
    )
    await state.set_state(ScienceSearchingParametersStates.terms)


@router.message(
    StateFilter(ScienceSearchingParametersStates.terms),
    ~F.text.in_({LEXICON_RUS['finished'], LEXICON_RUS['back']}),
    TextSearchingParametersFilters()
)
async def process_terms_sent_parameters(message: Message, valid_parameters: list[str], state: FSMContext):
    await update_state_data(
        state_name=StatesName.TERMS,
        concatenated=True,
        parameters=valid_parameters,
        state=state
    )
    await message.answer(text='Обнаруженные ключевые слова сохранены!\n\n')


# source_published
@router.message(StateFilter(default_state), F.text == LEXICON_RUS['source_published'])
async def process_source_published_parameters(message: Message, state: FSMContext):
    await message.answer(
        text='Введите название журнала(elsavier): ',
        reply_markup=finished_entering_parameters_keyboards()
    )
    await state.set_state(ScienceSearchingParametersStates.source_published)


@router.message(
    StateFilter(ScienceSearchingParametersStates.source_published),
    ~F.text.in_({LEXICON_RUS['finished'], LEXICON_RUS['back']}),
    TextSearchingParametersFilters()
)
async def process_source_published_sent_parameters(message: Message, valid_parameters: list[str], state: FSMContext):
    await update_state_data(
        state_name=StatesName.SOURCE_PUBLISHED,
        concatenated=True,
        parameters=valid_parameters,
        state=state
    )
    await message.answer(text='Журнал/издание сохранены!\n\n')


# authors
@router.message(StateFilter(default_state), F.text == LEXICON_RUS['authors'])
async def process_authors_parameters(message: Message, state: FSMContext):
    await message.answer(
        text='Введите авторов(John Smith, Ivan Susanin): ',
        reply_markup=finished_entering_parameters_keyboards()
    )
    await state.set_state(ScienceSearchingParametersStates.authors)


@router.message(
    StateFilter(ScienceSearchingParametersStates.authors),
    ~F.text.in_({LEXICON_RUS['finished'], LEXICON_RUS['back']}),
    TextSearchingParametersFilters()
)
async def process_authors_sent_parameters(message: Message, valid_parameters: list[str], state: FSMContext):
    await update_state_data(
        state_name=StatesName.AUTHORS,
        concatenated=True,
        parameters=valid_parameters,
        state=state
    )
    await message.answer(text='Имена авторов сохранены!\n\n')


# years
@router.message(StateFilter(default_state), F.text == LEXICON_RUS['years'])
async def process_years_parameters(message: Message, state: FSMContext):
    await message.answer(
        text='Введите год выхода работы (1999, или 1999-2010):',
        reply_markup=finished_entering_parameters_keyboards()
    )
    await state.set_state(ScienceSearchingParametersStates.years)


@router.message(
    StateFilter(ScienceSearchingParametersStates.years),
    ~F.text.in_({LEXICON_RUS['finished'], LEXICON_RUS['back']}),
    YearsSearchingParametersFilters()
)
async def process_years_sent_parameters(message: Message, valid_parameters: list[int], state: FSMContext):
    await update_state_data(
        state_name=StatesName.YEARS,
        concatenated=False,
        parameters=valid_parameters,
        state=state
    )
    await message.answer(text='Год выпуска сохранен!\n\n')


# pages
@router.message(StateFilter(default_state), F.text == LEXICON_RUS['pages'])
async def process_pages_parameters(message: Message, state: FSMContext):
    await message.answer(
        text='Введите количество страниц(50, или 50-100)',
        reply_markup=finished_entering_parameters_keyboards()
    )
    await state.set_state(ScienceSearchingParametersStates.pages)


@router.message(
    StateFilter(ScienceSearchingParametersStates.pages),
    ~F.text.in_({LEXICON_RUS['finished'], LEXICON_RUS['back']}),
    PagesSearchingParametersFilters()
)
async def process_pages_sent_parameters(message: Message, valid_parameters: list[str], state: FSMContext):
    await update_state_data(
        state_name=StatesName.PAGES,
        concatenated=False,
        parameters=valid_parameters,
        state=state
    )
    await message.answer(text='Количество страниц сохранено!\n\n')


# back button to choose topic entering words
@router.message(
    StateFilter(ScienceSearchingParametersStates.source_published),
    F.text == LEXICON_RUS['back']
)
@router.message(StateFilter(ScienceSearchingParametersStates.terms), F.text == LEXICON_RUS['back'])
@router.message(StateFilter(ScienceSearchingParametersStates.authors), F.text == LEXICON_RUS['back'])
@router.message(StateFilter(ScienceSearchingParametersStates.years), F.text == LEXICON_RUS['back'])
@router.message(StateFilter(ScienceSearchingParametersStates.pages), F.text == LEXICON_RUS['back'])
async def back_to_basic_keyboard(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(text='Возвращаемся к выбору тему', reply_markup=get_searching_parameters_keyboard())


# finish entering parameters
@router.message(StateFilter(default_state), F.text == LEXICON_RUS['finished'])
async def finish_entering_parameters(message: Message, state: FSMContext, database: AsyncBotDatabase):
    await upload_data_and_reset_state(
        user_id=message.from_user.id,
        state=state,
        database=database
    )
    await message.answer(text='finish entering parameters message', reply_markup=get_started_keyboard())


# invalid behavior
@router.message(
    StateFilter(
        ScienceSearchingParametersStates.terms,
        ScienceSearchingParametersStates.source_published,
        ScienceSearchingParametersStates.authors,
        ScienceSearchingParametersStates.years,
        ScienceSearchingParametersStates.pages
    )
)
async def incorrect_terms_parameters(message: Message, state: FSMContext):
    await message.answer(text='Кажется вы ввели неправильные данные!\n\n'
                              'Выберите пункт в меню и попробуйте снова!\n\n')
