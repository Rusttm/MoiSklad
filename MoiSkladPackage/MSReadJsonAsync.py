import json
import os
import re
import asyncio
import aiofiles


class MSReadJsonAsync:
    """read and return data from json file"""
    logger_name = f"{os.path.basename(__file__)}"
    dir_name = "data"
    config_dir_name = "config"
    config_file_name = "ms_main_config.json"
    _module_config = None

    def __init__(self):
        super().__init__()
        self.set_module_config_sync()

    def set_module_config_sync(self):
        self._module_config = self.get_json_data_sync(dir_name=self.config_dir_name, file_name=self.config_file_name)

    def get_json_data_sync(self, dir_name, file_name) -> dict:
        """ extract data from MS json file
        return dict """
        data = dict()
        try:
            file_dir = os.path.dirname(__file__)
            if not re.search('json', file_name):
                file_name += '.json'
            CONF_FILE_PATH = os.path.join(file_dir, dir_name, file_name)
            with open(CONF_FILE_PATH, 'r') as json_file:
                json_data = json_file.read()
            data = json.loads(json_data)
            # self.logger.debug(f"{__class__.__name__} got data from json file")
        except Exception as e:
            print(f"{__class__.__name__} can't get json file!{e}")
            # self.logger.error(f"{__class__.__name__} can't read json file!{e}")
        return data

    async def get_json_data_async(self, dir_name, file_name) -> dict:
        """ extract data from MS json file
        return dict """
        data = dict()
        try:
            file_dir = os.path.dirname(__file__)
            if not re.search('json', file_name):
                file_name += '.json'
            CONF_FILE_PATH = os.path.join(file_dir, dir_name, file_name)
            async with aiofiles.open(CONF_FILE_PATH, 'r') as json_file:
                json_data = await json_file.read()
            data = json.loads(json_data)
            # self.logger.debug(f"{__class__.__name__} got data from json file")
        except Exception as e:
            print(f"{__class__.__name__} can't get json file!{e}")
            # self.logger.error(f"{__class__.__name__} can't read json file!{e}")
        return data


if __name__ == '__main__':
    # connector = MSReadJsonAsync()
    # print(connector.get_config_json_data_sync(file_name='url_money.json'))
    connector2 = MSReadJsonAsync()
    # print(connector2.get_json_data_sync())
    print(asyncio.run(connector2.get_json_data_async("config", "ms_balances_config.json")))
