import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType
# from AiogramPackage.TGKeyboards import TGKeybReplyMarkup as my_reply_kb
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1, reply_kb_lvl2, del_kb
from AiogramPackage.TGKeyboards.TGKeybReplyList import make_row_keyboard

user_router = Router()
user_router.message.filter(BOTFilterChatType(["private"]))


@user_router.message(CommandStart())
@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
@user_router.message(F.text.lower() == "start")
async def start_cmd(message: types.Message):
    # version1
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!", reply_markup=my_reply_kb.my_reply_kb)
    # version2
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to bot!",
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
    brand = State(),
    model = State()

available_instrument_brands = ["Block", "Meite"]
available_instrument_models = ["812", "CN50"]

@user_router.message(StateFilter(None), F.text == "Инструмент")
async def find_brand_instrument(message: types.Message, state: FSMContext):
    await message.answer(f"Введите <b>Марку</b> инструмента", reply_markup=make_row_keyboard(available_instrument_brands))
    await state.set_state(FindInstrument.brand)

@user_router.message(FindInstrument.brand)
async def find_brand_instrument(message: types.Message):
    await message.answer(f"Введена невернаф марка! Введите <b>Марку</b> инструмента",
                         reply_markup=make_row_keyboard(available_instrument_brands))


# @user_router.message(FindInstrument.brand, F.text.in_(available_instrument_brands))
# async def find_model_instrument(message: types.Message, state: FSMContext):
#     await state.update_data(brand=message.text)
#     await message.answer(f"Введите <b>Модель</b> инструмента", reply_markup=make_row_keyboard(available_instrument_models))
#     await state.set_state(FindInstrument.model)
#     current_state = await state.get_state()
#     print(f"{current_state=}")


@user_router.message(FindInstrument.model, F.text.in_(available_instrument_models))
async def find_instrument(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer(f"<b>Поиск</b> инструмента", reply_markup=reply_kb_lvl2.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Что Вас интересует?"
    ))
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


@user_router.message(Command("cancel", ignore_case=True))
@user_router.message(F.text.casefold() == "Отмена")
async def cancel_find_instrument(message: types.Message, state: FSMContext):
    await message.answer(f"Ввод <b>Отменен</b>", reply_markup=
    reply_kb_lvl2.as_markup(resize_keyboard=True, input_field_placeholder="Что Вас интересует?"))


@user_router.message(Command("back", ignore_case=True))
@user_router.message(F.text.casefold() == "Назад")
async def cancel_find_instrument(message: types.Message, state: FSMContext):
    await message.answer(f"<b>Возврат</b> к прошлому шагу")
