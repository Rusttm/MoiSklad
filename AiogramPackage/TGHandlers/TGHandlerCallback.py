import datetime
import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot, flags
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.callback_answer import CallbackAnswer
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
        await callback.answer("🆘Ошибка!")
        await callback.message.answer(msg)
    else:
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        await callback.answer(f"Формирую отчет по 💸прибыли {extra_data}:")
        await callback.message.answer(f"<a href='{gs_href}'>💸Прибыль по месяцу: {int(total)}руб..</a>")

@callback_router.callback_query(F.data.startswith("rep_fin_balance_"), BOTFilterFinList())
# @flags.callback_answer(pre=False, cache_time=60)
async def get_rep_bal(callback: types.CallbackQuery, callback_answer: CallbackAnswer):
    extra_data = callback.data[16:]
    try:
        from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
        controller = MSGSControllerAsync()
        res_dict = await controller.save_balance_gs_async()
        print(f"{res_dict=}")
    except Exception as e:
        msg = f"Can't form balance report, Error:\n {e}"
        logging.warning(msg)
        await callback.answer("🆘Ошибка!", cache_time=60)
        await callback.message.answer(msg)
    else:
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        await callback.answer(f"Формирую отчет по ⚖️балансам {extra_data}:", cache_time=60)
        await callback.message.answer(f"<a href='{gs_href}'>Итоговый ⚖️баланс на сегодня: {int(total)}руб.</a>")

@callback_router.callback_query(F.data.startswith("rep_fin_debt_"), BOTFilterFinList())
async def get_rep_debt(callback: types.CallbackQuery):
    extra_data = callback.data[13:]
    try:
        from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
        controller = MSGSControllerAsync()
        res_dict = await controller.save_daily_debt_gs_async()
    except Exception as e:
        msg = f"Can't form debt report, Error:\n {e}"
        logging.warning(msg)
        await callback.answer("Ошибка!")
        await callback.message.answer(msg)
    else:
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        await callback.answer(f"Формирую отчет по 🚬задолженностям {extra_data}:")
        await callback.message.answer(f"<a href='{gs_href}'>🚬Задолженность клиентов на сегодня: {int(total)}руб..</a>")

@callback_router.callback_query(F.data.startswith("rep_fin_margin_"), BOTFilterFinList())
async def get_rep_margins(callback: types.CallbackQuery):
    extra_data = callback.data[15:]
    try:
        from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
        controller = MSGSControllerAsync()
        res_dict = await controller.save_daily_margins_gs_async()
        print(f"{res_dict=}")
    except Exception as e:
        msg = f"Can't form margins report, Error:\n {e}"
        logging.warning(msg)
        await callback.answer("Ошибка!")
        await callback.message.answer(msg)
    else:
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        await callback.answer(f"Формирую отчет минимальным отгрузкам {extra_data}:")
        if total == 0:
            await callback.message.answer(f"<a href='{gs_href}'>🛠️Отгрузок меньше 30% нет 🔦</a>")
        else:
            await callback.message.answer(f"<a href='{gs_href}'>🛠️Отгрузок меньше 30%: {int(total)}шт.</a>")
            margins_list = res_dict.get("data")[0]
            for client_dict in margins_list:
                await callback.message.answer(f"{client_dict.get('name')}: {client_dict.get('sale')}руб ({client_dict.get('profitability')}%) \n")


@callback_router.callback_query(F.data.startswith("rep_fin_account_"), BOTFilterFinList())
async def get_rep_account(callback: types.CallbackQuery):
    extra_data = callback.data[16:]
    try:
        from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
        controller = MSGSControllerAsync()
        res_dict = await controller.save_daily_accounts_gs_async()
        print(f"{res_dict=}")
    except Exception as e:
        msg = f"Can't form margins report, Error:\n {e}"
        logging.warning(msg)
        await callback.answer("Ошибка!")
        await callback.message.answer(msg)
    else:
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        await callback.answer(f"Формирую отчет по остаткам на счетах {extra_data}:")
        if total == 0:
            await callback.message.answer(f"<a href='{gs_href}'>💰Денег на счетах нет 🙅‍</a>")
        else:
            await callback.message.answer(f"<a href='{gs_href}'>Всего 💰денег на счетах: {int(total)}руб..</a>")


@callback_router.callback_query(F.data.startswith("rep_fin_daily_"), BOTFilterFinList())
async def get_rep_daily(callback: types.CallbackQuery):
    extra_data = callback.data[16:]
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res_msg = str(f"Отчет на {today}\n")
    try:
        from MoiSkladPackage.MSControllers.MSGSControllerAsync import MSGSControllerAsync
        controller = MSGSControllerAsync()
        # 1 string -accounts
        account_res_dict = await controller.save_daily_accounts_gs_async()
        gs_href = account_res_dict.get("info").get("gs_href")
        total = account_res_dict.get("info").get("total")
        res_msg += f"<a href='{gs_href}'>💰Денег на <b>счетах:</b> {int(total)}руб.</a>\n"
        # 2 string -debts
        res_dict = await controller.save_daily_debt_gs_async()
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        res_msg += f"<a href='{gs_href}'>🚬<b>Задолженность</b> клиентов на сегодня: {int(total)}руб.</a>\n"
        # 3 string -profit
        res_dict = await controller.save_profit_gs_daily_async()
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        res_msg += f"<a href='{gs_href}'>💸<b>Прибыль</b> по месяцу: {int(total)}руб.</a>\n"
        # 4 string -balance
        res_dict = await controller.save_balance_gs_async()
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")
        res_msg += f"<a href='{gs_href}'>Итоговый ⚖️<b>Баланс</b> на сегодня: {int(total)}руб.</a>\n"
        # 5 string - margin sales
        # res_dict = await controller.save_daily_margins_gs_async()
        res_dict = await controller.save_custom_margins_gs_async(from_date="2023-01-9", to_date="2023-01-9")
        gs_href = res_dict.get("info").get("gs_href")
        total = res_dict.get("info").get("total")

        if total == 0:
            res_msg += f"<a href='{gs_href}'>🛠️<b>Отгрузок</b> меньше 30% нет 🔦</a>"
        else:
            res_msg += f"<a href='{gs_href}'>🛠️<b>Отгрузок</b> меньше 30%: {int(total)}шт.</a>\n"
            margins_list = res_dict.get("data")[0]
            temp_str = str()
            for client_dict in margins_list:
                temp_str += f"{client_dict.get('name')}: {client_dict.get('sale')}руб ({client_dict.get('profitability')}%) \n"
            res_msg += temp_str
    except Exception as e:
        msg = f"Can't form margins report, Error:\n {e}"
        logging.warning(msg)
        await callback.answer("Ошибка!")
        await callback.message.answer(msg)
    else:
        await callback.message.answer(res_msg, cache_time=120)
