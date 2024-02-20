""" модерация группы в которой бот является админом"""

import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot, html
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN, StateFilter, CommandObject
# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.deep_linking import create_start_link

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterIsGroupAdmin, \
    BOTFilterAdminList
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1_admin, del_kb, reply_kb_lvl2_admin
from AiogramPackage.TGAlchemy.TGDbQueriesEvent import db_add_event
from AiogramPackage.TGAlchemy.TGModelEvent import TGModelEvent

admin_group_router = Router()
admin_group_router.message.filter(BOTFilterChatType(["private"]), BOTFilterAdminList())


# admin_group_router.edited_message.filter(BOTFilterChatType(["private", "group", "supergroup"]), BOTFilterAdminList())
class SavePhoto(StatesGroup):
    event_img = State()


class DownLoadFile(StatesGroup):
    download_file = State()

# class DownLoadFile(StatesGroup):
#     download_file = State()


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))


async def reload_admins_list(bot: Bot):
    """ some lists should be reloaded by /admin command"""
    _main_key = "bot_config"
    _admin_key = "admin_members"
    _fin_key = "fin_members"
    _restricted_key = "restricted_words"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _static_dir = "data_static"
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


@admin_group_router.message(Command("admin", ignore_case=True))
async def admin_cmd(message: types.Message, bot: Bot):
    """ this handler reloads group admins list"""
    await reload_admins_list(bot=bot)
    await message.delete()


@admin_group_router.message(Command("report", "rep", ignore_case=True))
@admin_group_router.message(F.text.lower().contains("отчеты"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>reports!</b>", reply_markup=
    reply_kb_lvl2_admin.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Какой отчет Вас интересует?"))
    logging.info("requested reports")


@admin_group_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin main menu!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))


@admin_group_router.message(Command("photo", "foto", ignore_case=True))
@admin_group_router.message(StateFilter(None), F.text == "photo")
async def start_save_img(message: types.Message, state: FSMContext):
    # current_state = await state.get_state()
    # if current_state is None:
    #     return
    # await state.clear()
    await state.set_state(SavePhoto.event_img)
    await message.answer("Загрузите фото")


@admin_group_router.message(SavePhoto.event_img, F.photo)
async def add_event_img(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(image=message.photo[-1].file_id)
    print(f"{message.caption=}")

    data_dict = await state.get_data()
    # if not data_dict:
    #     data_dict = dict()
    data_dict = dict()
    data_dict["from_chat_id"] = message.from_user.id
    data_dict["to_chat_id"] = message.chat.id
    data_dict["event_msg"] = "сообщение:" + str(message.text)
    data_dict["event_descr"] = "описание:" + str(message.text)
    data_dict["event_img"] = message.photo[-1].file_id
    try:
        await db_add_event(session, data_dict)
        file_name = message.photo[-1].file_id
        static_file = os.path.join(os.getcwd(), "data_static", f"{file_name}.jpg")
        print(f"{static_file=}")
        await bot.download(message.photo[-1], destination=static_file)
    except Exception as e:
        msg = f"Не смог добавить фото и сообщение в базу, ошибка: \n {e}"
        await message.answer(msg)
    else:
        await message.answer("photo added to db and downloaded")
        # link = await create_start_link(bot, f"download?{file_name}.jpg")
        # await message.answer(f"go to tag: {link}")
        await message.answer(f"/download {file_name}.jpg")
        await message.answer(f"download_{file_name}.jpg")
    await state.clear()


#
@admin_group_router.message(SavePhoto.event_img)
async def add_event_img(message: types.Message):
    await message.answer("photo not added, please send me a photo")


# from https://mastergroosha.github.io/aiogram-3-guide/messages/
@admin_group_router.message(Command("download"))
@admin_group_router.message(StateFilter(None), F.text.lower() == "download")
async def cmd_download(message: types.Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await state.set_state(DownLoadFile.download_file)
        await message.answer("Введите название файла")
        # return
    else:
        # await state.update_data(file_name=command.args)
        # return
        try:
            file_name = command.args
            static_file = os.path.join(os.getcwd(), "data_static", file_name)
            async with aiofiles.open(static_file, 'rb') as image_from_buffer:
                result = await message.answer_photo(
                    BufferedInputFile(file=await image_from_buffer.read(), filename=file_name),
                    caption=f"{file_name}")
        except Exception as e:
            msg = f"Cant load file from destination, Error: \n {e}"
            await message.answer(msg)
        else:
            await message.answer(f"Файл {file_name} отправлен!")

@admin_group_router.message(DownLoadFile.download_file)
@admin_group_router.message(F.text.lower().startswith("download_"))
async def save_static_img(message: types.Message, state: FSMContext):
    """  downloading and sending img from bot static directory"""
    if message.text.startswith("download_"):
        file_name = message.text[9:]
    else:
        try:
            current_state = await state.get_state()
            if current_state == DownLoadFile.download_file:
                data_dict = await state.get_data()
                file_name = data_dict.get("file_name", None)
                if not file_name:
                    file_name = message.text
        except Exception as e:
            msg = f"cant get file_name info, Error \n {e}"
            print(msg)
    await message.answer(f"Отправляю файл ...")
    try:
        static_file = os.path.join(os.getcwd(), "data_static", file_name)
        async with aiofiles.open(static_file, 'rb') as file_from_buffer:
            result = await message.answer_document(
                BufferedInputFile(file=await file_from_buffer.read(), filename=f"bot_{file_name}"), caption=f"Загрузите файл")
    except Exception as e:
        msg = f"Cant load file from destination, Error: \n {e}"
        await message.answer(msg)
    else:
        await message.answer(f"Файл отправлен")
    await state.clear()
    return


@admin_group_router.message(CommandStart())
@admin_group_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(f"Hi, {html.quote(message.from_user.first_name)}, welcome to admin start command details!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))
