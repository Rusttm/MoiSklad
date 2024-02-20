import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.filters.callback_data import CallbackQueryFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType
# from AiogramPackage.TGKeyboards import TGKeybReplyMarkup as my_reply_kb
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1, reply_kb_lvl2, del_kb
from AiogramPackage.TGKeyboards.TGKeybReplyList import make_row_keyboard
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns, get_url_btns, get_mixed_btns
from AiogramPackage.TGAlchemy.TGModelProd import TGModelProd
from AiogramPackage.TGAlchemy.TGDbQueriesProd import db_get_prod

user_router = Router()
user_router.message.filter(BOTFilterChatType(["private"]))


@user_router.message(CommandStart())
@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
@user_router.message(F.text.lower() == "start")
async def start_cmd(message: types.Message):
    # version1
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!", reply_markup=my_reply_kb.my_reply_kb)
    # version2
    await message.answer(f"Hi, {hbold(message.from_user.first_name)}, welcome to bot!",
                         reply_markup=reply_kb_lvl1.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует"
                         ))
    # version 3
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!",
    #                      reply_markup=my_bld_kb.get_my_kb(
    #                          "Меню",
    #                          "О боте",
    #                          "Реквизиты Компании",
    #                          "Платежные реквизиты",
    #                          placeholder="Выберите пункт меню",
    #                          sizes=(2, 2)
    #                      )
    #                      )


@user_router.message(Command("hide_menu", ignore_case=True))
async def menu_cmd(message: types.Message):
    # ver1
    await message.answer(f"{message.from_user.first_name}, can't hide main menu!", reply_markup=del_kb)


@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=reply_kb_lvl1)


@user_router.message(Command("catalogue", ignore_case=True))
@user_router.message((F.text.lower().contains("каталог")) | (F.text.lower().contains("catalogue")))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>Catalogue</b>",
                         reply_markup=reply_kb_lvl2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))


class FindInstrument(StatesGroup):
    brand = State()
    model = State()

class FindSpare(StatesGroup):
    brand = State()
    code = State()

available_instrument_brands = []
available_instrument_models = ["812", "CN70"]
add_btn = ["Отмена"]


@user_router.message(StateFilter('*'), Command("cancel", ignore_case=True))
@user_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_find_instrument(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Ввод <b>Отменен</b>", reply_markup=
    reply_kb_lvl2.as_markup(resize_keyboard=True, input_field_placeholder="Что Вас интересует?"))


@user_router.message(StateFilter(None), F.text == "Инструмент")
async def find_brand_instrument(message: types.Message, state: FSMContext, bot: Bot):
    available_instrument_brands = bot.filters_dict.get("instrument_brands_list", ["Meite", "Block"])
    kb_lines = [add_btn, available_instrument_brands]
    await message.answer(f"Введите <b>Марку</b> инструмента", reply_markup=make_row_keyboard(kb_lines))
    await state.set_state(FindInstrument.brand)


# @user_router.message(FindInstrument.brand, F.text.in_(available_instrument_brands))
@user_router.message(FindInstrument.brand)
async def find_model_instrument(message: types.Message, state: FSMContext, bot: Bot):
    available_instrument_models = bot.filters_dict.get("instrument_models_list", ["8016", "851", "CN"])
    kb_lines = [add_btn, available_instrument_models]
    await state.update_data(brand=message.text)
    await message.answer(f"Введите <b>Модель</b> инструмента", reply_markup=make_row_keyboard(kb_lines))
    await state.set_state(FindInstrument.model)


# @user_router.message(FindInstrument.brand, F.text.lower() != "отмена")
# async def wrong_brand_instrument(message: types.Message):
#     kb_lines = [add_btn, available_instrument_brands]
#     await message.answer(f"Введена неверная марка! Введите <b>Марку</b> инструмента",
#                          reply_markup=make_row_keyboard(kb_lines))


# @user_router.message(FindInstrument.model, F.text.in_(available_instrument_models))
@user_router.message(FindInstrument.model)
async def find_instrument(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(model=message.text)
    await message.answer(f"<b>Поиск</b> инструмента", reply_markup=reply_kb_lvl2.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Что Вас интересует?"
    ))
    data = await state.get_data()
    brand = data.get("brand")
    model = data.get("model")
    statement = select(TGModelProd).filter(TGModelProd.name.contains(brand)).filter(TGModelProd.name.contains(model))
    result = await session.execute(statement)
    obj_list = result.scalars().all()
    if obj_list:
        for prod_obj in obj_list:
            static_file = os.path.join(os.getcwd(), "data_static", "instrument_img.jpg")
            async with aiofiles.open(static_file, "rb") as plot_img:
                print(f"{len(prod_obj.id)=} and {len(prod_obj.meta.get('href'))=}")
                url = prod_obj.meta.get('href')
                await bot.send_photo(chat_id=message.chat.id,
                                     photo=BufferedInputFile(file=await plot_img.read(), filename="Инструмент"),
                                     caption=f"Инструмент {prod_obj.name}",
                                     reply_markup=get_mixed_btns(btns={
                                         "Перейти": f"{prod_obj.meta.get('uuidHref')}",
                                         "Подробнее": f"get_prod_info_{prod_obj.id}"
                                     }))

    else:
        await message.answer(f"Инструмента {str(data)} не обнаружено!")
    await state.clear()



"""  Запчасти """

@user_router.message(StateFilter(None), F.text.lower() == "запчасти")
async def find_brand_spare(message: types.Message, state: FSMContext, bot: Bot):
    available_spares_brands = bot.filters_dict.get("spares_brands_list", ["Meite", "Block"])
    kb_lines = [add_btn, available_spares_brands]
    await message.answer(f"Введите <b>строку</b> для поиска запчасти", reply_markup=make_row_keyboard(kb_lines))
    await state.set_state(FindSpare.brand)

@user_router.message(FindSpare.brand)
async def find_model_spare(message: types.Message, state: FSMContext, bot: Bot):
    available_spares_codes = bot.filters_dict.get("spare_codes_list", ["8016", "851", "CN"])
    kb_lines = [add_btn, available_spares_codes]
    await state.update_data(brand=message.text)
    await message.answer(f"Введите <b>код</b> запчасти",
                         reply_markup=make_row_keyboard(kb_lines),
                         input_field_placeholder="Введите поисковый запрос")
    await state.set_state(FindSpare.code)
@user_router.message(FindSpare.code)
async def find_spare(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(code=message.text)
    await message.answer(f"<b>Поиск</b> инструмента", reply_markup=reply_kb_lvl2.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Введите поисковый запрос"
    ))
    data = await state.get_data()
    brand = data.get("brand")
    code = data.get("code")
    statement = select(TGModelProd).filter(TGModelProd.pathName.contains(brand)).filter(TGModelProd.name.contains(code))
    result = await session.execute(statement)
    obj_list = result.scalars().all()
    if obj_list:
        for prod_obj in obj_list:
            static_file = os.path.join(os.getcwd(), "data_static", "spares_img2.jpg")
            async with aiofiles.open(static_file, "rb") as plot_img:
                print(f"{len(prod_obj.id)=} and {len(prod_obj.meta.get('href'))=}")
                url = prod_obj.meta.get('href')
                await bot.send_photo(chat_id=message.chat.id,
                                     photo=BufferedInputFile(file=await plot_img.read(), filename="Инструмент"),
                                     caption=f"Запчасти {prod_obj.name}",
                                     reply_markup=get_mixed_btns(btns={
                                         "Перейти": f"{prod_obj.meta.get('uuidHref')}",
                                         "Подробнее": f"get_prod_info_{prod_obj.id}"
                                     }))

    else:
        await message.answer(f"Запчастей: {str(data)} не обнаружено!")
    await state.clear()


# @user_router.message(FindInstrument.model, F.text.lower() != "отмена")
# async def wrong_model_instrument(message: types.Message):
#     kb_lines = [add_btn, available_instrument_models]
#     await message.answer(f"Введена неверная модель! Введите <b>Модель</b> инструмента",
#                          reply_markup=make_row_keyboard(kb_lines))


# @user_router.message(StateFilter('*'), Command("back", ignore_case=True))
# @user_router.message(StateFilter('*'), F.text.casefold() == "назад")
# async def cancel_find_instrument(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state == FindInstrument.brand:
#         await message.answer(f"предыдущего шага нет, нажмите кнопку Отмена")
#         return
#     prev = None
#     for step in FindInstrument.__all_states__:
#         if step.state == current_state:
#             await state.set_state(prev)
#             await message.answer(f"<b>Возврат</b> к прошлому шагу")
#             return
#         prev = step
