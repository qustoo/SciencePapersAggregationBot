from aiogram import F, Router
from aiogram.types import Message
from src.lexicons.lexicon_rus import LEXICON_RUS
from src.external_service.service import external_api
from src.database import db

external_science_router = Router()


@external_science_router.message(F.text == LEXICON_RUS['run_aggregation_papers'])
async def run_search_science_api(message: Message):
    terms, source, authors, min_years, max_years, min_pages, max_pages = await db.fetch_last_entered_parameters(
        user_id=message.from_user.id
    )
    science_papers = await external_api.get_works(
        terms=terms,
        source_name=source,
        author_name=authors,
        year_begin=min_years,
        year_end=max_years,
        pages_min=min_pages,
        pages_max=max_pages,
    )
    print(f'{science_papers=}')
