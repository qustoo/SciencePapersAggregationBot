import re

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from src.consts import OPEN_ALEX_URL_PATTERN


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, str]:
        link_data, del_ends = callback.data.split('_')
        matched_link = re.match(pattern=OPEN_ALEX_URL_PATTERN, string=link_data)
        if matched_link and del_ends == 'delete':
            return {'paper_link': link_data}
        return False
