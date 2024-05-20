from src.lexicons.lexicon_rus import LEXICON_RUS
from aiogram import F, Router
from aiogram.types import Message
from src.consts import ENTERED_PARAMETERS_PATTERN, DATA_IS_NOT_SET
from src.database import db

entered_parameters_router = Router()


@entered_parameters_router.message(F.text == LEXICON_RUS['entered_parameters'])
async def check_entered_parameters(message: Message):
    terms, source, authors, min_years, max_years, min_pages, max_pages = await db.fetch_last_entered_parameters(
        user_id=message.from_user.id
    )
    await message.answer(text=ENTERED_PARAMETERS_PATTERN.format(
        terms=terms or DATA_IS_NOT_SET,
        source=source or DATA_IS_NOT_SET,
        authors=authors or DATA_IS_NOT_SET,
        min_years=min_years or DATA_IS_NOT_SET,
        max_years=max_years or DATA_IS_NOT_SET,
        min_pages=min_pages or DATA_IS_NOT_SET,
        max_pages=max_pages or DATA_IS_NOT_SET
    ))
