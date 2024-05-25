from aiogram import Router
from aiogram.types import Message

from src.lexicons.lexicon_rus import LEXICON_RUS

router = Router()


@router.message()
async def catch_invalid_messages(message: Message):
    await message.answer(text=LEXICON_RUS['error'])
