from MSMainClass import MSMainClass
import json
import os
import re
import asyncio
import aiofiles


class MSReadJsonAsync(MSMainClass):
    """read and return data from json file"""
    logger_name = "jsonreaderasync"
    dir_name = "data"

    async def get_config_json_data_async(self, file_name=None) -> dict:
        """ extract data from MS json file
        return dict """
        data = dict()
        if file_name:
            try:
                file_dir = os.path.dirname(__file__)
                if not re.search('json', file_name):
                    file_name += '.json'
                CONF_FILE_PATH = os.path.join(file_dir, self.dir_name, file_name)
                async with aiofiles.open(CONF_FILE_PATH, 'r') as json_file:
                    json_data = await json_file.read()
                data = json.loads(json_data)
                self.logger.debug(f"{__class__.__name__} got data from json file")
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} can't read json file!{e}")
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    "Please, declare existing json file name with 'file_name='")
        return data

    def get_config_json_data_sync(self, file_name=None) -> dict:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.get_config_json_data_async(file_name=file_name))
        # result = asyncio.run(self.get_config_json_data_async(file_name=file_name))
        return result

if __name__ == '__main__':
    connector = MSReadJsonAsync()
    print(connector.get_config_json_data_sync(file_name='url_money.json'))
