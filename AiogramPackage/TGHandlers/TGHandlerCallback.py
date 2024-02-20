import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType
from AiogramPackage.TGAlchemy.TGDbQueriesProd import db_get_prod

callback_router = Router()
callback_router.message.filter(BOTFilterChatType(["private"]))


@callback_router.callback_query(F.data.startwith("get_info"))
async def get_prod_info(callback: types.CallbackQuery, session: AsyncSession):
    prod_id = callback.data[8:]
    prod_data_dict = await db_get_prod(prod_id=prod_id, session=session)
    prod_name = prod_data_dict.get("name", "unknown")
    await callback.answer(f"Получите свой товар: {prod_name}")
    await callback.message.answer("Товар получили, спасибо!")

