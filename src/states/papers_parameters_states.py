from aiogram.filters.state import State, StatesGroup


class ScienceSearchingParametersStates(StatesGroup):
    terms = State()
    source_published = State()
    authors = State()
    years = State()
    pages = State()
