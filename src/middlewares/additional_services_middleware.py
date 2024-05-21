from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database import AsyncBotDatabase
from src.external_service.api import ExternalScienceAPI


class DataBaseMiddleware(BaseMiddleware):
    def __init__(self, db_name: str):
        super().__init__()
        self.db_name = db_name

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['database'] = AsyncBotDatabase(self.db_name)
        data['external_service'] = ExternalScienceAPI()
        return await handler(event, data)
