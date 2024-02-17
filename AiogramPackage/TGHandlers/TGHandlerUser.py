import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.markdown import hbold
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType
# from AiogramPackage.TGKeyboards import TGKeybReplyMarkup as my_reply_kb
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1, reply_kb_lvl2


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
    await message.answer(f"{message.from_user.first_name}, can't hide main menu!", reply_markup=my_bld_kb.del_kb)

@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.my_reply_kb)


@user_router.message(Command("catalogue", ignore_case=True))
@user_router.message((F.text.lower().contains("каталог")) | (F.text.lower().contains("catalogue")))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>Catalogue</b>",
                         reply_markup=reply_kb_lvl2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))


