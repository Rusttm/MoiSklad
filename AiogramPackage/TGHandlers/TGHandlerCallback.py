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

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList
from AiogramPackage.TGAlchemy.TGDbQueriesProd import db_get_prod

callback_router = Router()
callback_router.message.filter(BOTFilterChatType(["private"]))


@callback_router.callback_query(F.data.startswith("get_prod_info_"), BOTFilterFinList())
async def get_prod_info(callback: types.CallbackQuery, session: AsyncSession):
    prod_id = callback.data[14:]
    prod_data = await db_get_prod(prod_id=prod_id, session=session)
    prod_description = prod_data.description
    # await callback.answer(f"Описание товара: {prod_description}", show_alert=True)
    await callback.message.answer(f"Описание товара: {prod_description}")

@callback_router.callback_query(F.data.startswith("rep_fin_profit_"), BOTFilterFinList())
async def get_rep_fin_profit(callback: types.CallbackQuery, session: AsyncSession):
    extra_data = callback.data[15:]
    try:
        from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
        controller = MSGSControllerAsync()
        res_dict = await controller.save_profit_gs_daily_async()
        print(f"{res_dict=}")
    except Exception as e:
        msg = f"Can't form daily profit report, Error:\n {e}"
        logging.warning(msg)
        await callback.answer("Ошибка!")
        await callback.message.answer(msg)
    else:
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        await callback.answer(f"Формирую отчет по прибыли {extra_data}:")
        await callback.message.answer(f"<a href='{gs_href}'>Прибыль по месяцу: {int(total)}руб..</a>")

@callback_router.callback_query(F.data.startswith("rep_fin_balance_"))
async def get_rep_fin_profit(callback: types.CallbackQuery, session: AsyncSession):
    extra_data = callback.data[16:]
    await callback.answer(f"Формирую балансовый отчет ... {extra_data}:")
    await callback.message.answer(f"Отчет по балансам {extra_data}")