from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Router
from aiogram.types import Message, TelegramObject


class CounterMiddleware(BaseMiddleware):
    """ example middleware"""
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)


router = Router()
router.message.middleware(CounterMiddleware())