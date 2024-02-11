import json
import os
import re
import asyncio
import aiofiles


class GSReadJsonAsync():
    """read and return data from json file"""
    logger_name = f"{os.path.basename(__file__)}"
    dir_name = "data"
    file_name = None
    conf_dir_name = "config"
    config_file_name = "gs_main_config.json"
    config_data = None

    def __init__(self, dir_name=None, file_name=None):
        super().__init__()
        if file_name:
            self.file_name = file_name
        if dir_name:
            self.dir_name = dir_name
        asyncio.run(self.get_config_json_data_async())

    async def get_json_data_async(self, dir_name=None, file_name=None) -> dict:
        """ extract data from json file return dict """
        if file_name:
            self.file_name = file_name
        else:
            file_name = self.file_name
        if dir_name:
            self.dir_name = dir_name

        data = dict()
        if file_name:
            try:
                file_dir = os.path.dirname(__file__)
                if not re.search('json', file_name):
                    file_name += '.json'
                CONF_FILE_PATH = os.path.join(file_dir, self.dir_name, self.file_name)
                async with aiofiles.open(CONF_FILE_PATH, 'r') as json_file:
                    json_data = await json_file.read()
                data = json.loads(json_data)
                # self.logger.debug(f"{__class__.__name__} got data from json file")
            except Exception as e:
                print(e)
                # self.logger.error(f"{__class__.__name__} can't read json file!{e}")
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    "Please, declare existing json file name with 'file_name='")
        return data

    def get_json_data_sync(self, file_name=None) -> dict:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.get_json_data_async(file_name=file_name))
        # result = asyncio.run(self.get_config_json_data_async(file_name=file_name))
        return result

    def get_config_json_data_sync(self, file_name=None) -> dict:
        # if not asyncio.get_event_loop():
        #     loop = asyncio.new_event_loop()
        # else:
        #     loop = asyncio.get_event_loop()
        result = asyncio.run(self.get_json_data_async(dir_name=self.conf_dir_name, file_name=self.config_file_name))
        # result = asyncio.run(self.get_config_json_data_async(file_name=file_name))
        self.config_data = result
        return result

    async def get_config_json_data_async(self, file_name=None) -> dict:
        self.config_data = await self.get_json_data_async(dir_name=self.conf_dir_name, file_name=self.config_file_name)
        return self.config_data

if __name__ == '__main__':
    # connector = MSReadJsonAsync()
    # print(connector.get_config_json_data_sync(file_name='url_money.json'))
    # connector2 = GSReadJsonAsync(dir_name="data", file_name="spread_sheet_metadata.json")
    # print(asyncio.run(connector2.get_json_data_async()))
    connector3 = GSReadJsonAsync()
    print(connector3.config_data)
    # print(connector3.get_config_json_data_sync())
