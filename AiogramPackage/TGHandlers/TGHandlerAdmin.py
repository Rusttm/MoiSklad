""" модерация группы в которой бот является админом"""

import logging

from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN
# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation
from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterIsGroupAdmin, BOTFilterAdminList
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_bld_admin, del_kb
from aiogram.utils.markdown import hbold

admin_group_router = Router()
admin_group_router.message.filter(BOTFilterChatType(["private"]), BOTFilterAdminList())
# admin_group_router.edited_message.filter(BOTFilterChatType(["private", "group", "supergroup"]), BOTFilterAdminList())



def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))

async def reload_admins_list(bot: Bot):
    _main_key = "bot_config"
    _admin_key = "admin_members"
    _fin_key = "fin_members"
    _restricted_key = "restricted_words"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _module_config: dict = None
    from AiogramPackage.TGConnectors.BOTReadJsonAsync import BOTReadJsonAsync
    connector = BOTReadJsonAsync()
    _module_config = await connector.get_main_config_json_data_async(_config_dir_name, _config_file_name)
    admin_members_dict = _module_config.get(_main_key).get(_admin_key)
    fin_members_dict = _module_config.get(_main_key).get(_fin_key)
    bot.admins_list = list(admin_members_dict.values())
    logging.info(f"reloaded {bot.admins_list=}")
    bot.fins_list = list(fin_members_dict.values())
    logging.info(f"reloaded {bot.fins_list=}")
    restricted_words_list = _module_config.get(_main_key).get(_restricted_key)
    bot.restricted_words = list(restricted_words_list)
    logging.info(f"reloaded {bot.restricted_words=}")
    # logging.info(f" now {bot.chat_group_admins_list=}")
    if not bot.chat_group_admins_list:
        bot.chat_group_admins_list = bot.admins_list
        logging.info(f" and {bot.chat_group_admins_list=}")
    # print(f"{bot.admins_list=}")


@admin_group_router.message(CommandStart())
@admin_group_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to admin start command details!",
                         reply_markup=reply_kb_bld_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))

@admin_group_router.message(Command("admin", ignore_case=True))
async def admin_cmd(message: types.Message, bot: Bot):
    """ this handler reloads group admins list"""
    await reload_admins_list(bot=bot)
    await message.delete()

@admin_group_router.message(Command("report", "rep", ignore_case=True))
@admin_group_router.message(F.text.lower().contains("отчет"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>reports!</b>")
    logging.info("requested reports")


@admin_group_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin main menu!",
                         reply_markup=reply_kb_bld_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))
