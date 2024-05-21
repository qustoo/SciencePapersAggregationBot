from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicons.lexicon_rus import LEXICON_RUS


def get_started_keyboard() -> ReplyKeyboardMarkup:
    fill_params = KeyboardButton(text=LEXICON_RUS['start_fill_based_parameters'])
    help_button = KeyboardButton(text=LEXICON_RUS['help'])
    entered_parameters = KeyboardButton(text=LEXICON_RUS['entered_parameters'])
    fetch_science_papers_button = KeyboardButton(text=LEXICON_RUS['run_aggregation_papers'])
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [fill_params, entered_parameters],
            [help_button, fetch_science_papers_button]
        ],
        resize_keyboard=True)
    return keyboard


def get_searching_parameters_keyboard() -> ReplyKeyboardMarkup:
    terms_button = KeyboardButton(text=LEXICON_RUS['terms'])
    source_published_button = KeyboardButton(text=LEXICON_RUS['source_published'])
    authors_button = KeyboardButton(text=LEXICON_RUS['authors'])
    years_button = KeyboardButton(text=LEXICON_RUS['years'])
    pages_button = KeyboardButton(text=LEXICON_RUS['pages'])
    finished_button = KeyboardButton(text=LEXICON_RUS['finished'])
    cancel_button = KeyboardButton(text=LEXICON_RUS['cancel'])
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [terms_button, authors_button, pages_button],
        [source_published_button, years_button],
        [finished_button],
        [cancel_button]
    ], resize_keyboard=True)
    return keyboard


def finished_entering_parameters_keyboards() -> ReplyKeyboardMarkup:
    back_button = KeyboardButton(text=LEXICON_RUS['back'])
    keyboard = ReplyKeyboardMarkup(keyboard=[[back_button]], resize_keyboard=True)
    return keyboard


def pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=LEXICON_RUS.get(button, button), callback_data=button) for button in buttons]
    builder.row(*buttons)
    return builder.as_markup()


def create_pagination_keyboard(page_number: int, total_pages: int) -> InlineKeyboardMarkup:
    middle_button = f'{page_number}/{total_pages}'
    if page_number == 1:
        return pagination_keyboard(middle_button, 'forward')
    elif 1 < page_number < total_pages:
        return pagination_keyboard('backward', middle_button, 'forward')
    return pagination_keyboard('backward', middle_button)


def start_reading_papers_keyboard() -> ReplyKeyboardMarkup:
    read_button = KeyboardButton(text=LEXICON_RUS['read'])
    back_button = KeyboardButton(text=LEXICON_RUS['back'])

    keyboard = ReplyKeyboardMarkup(keyboard=[[read_button, back_button]], resize_keyboard=True)
    return keyboard
