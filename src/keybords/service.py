from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
