from aiogram.filters import Filter
from aiogram import types
import os


class BOTFilterChat(Filter):

    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class BOTFilterFin(Filter):
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "bot_config"
    _fin_key = "fin_members"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _module_config: dict = None

    def __init__(self):
        """ filter for financial group members"""
        from AiogramPackage.TGConnectors.BOTReadJsonAsync import BOTReadJsonAsync
        self.connector = BOTReadJsonAsync()


    async def __call__(self, message: types.Message) -> bool:
        self._module_config = await self.connector.get_main_config_json_data_async(self._config_dir_name,
                                                                       self._config_file_name)
        fin_members_dict = self._module_config.get(self._main_key).get(self._fin_key)
        return message.from_user.id in list(fin_members_dict.values())

if __name__ == "__main__":
    filter = BOTFilterFin()
    print(filter._module_config)