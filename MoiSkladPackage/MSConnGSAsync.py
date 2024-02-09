# -*- coding: utf-8 -*-
# from https://gspread-asyncio.readthedocs.io/en/latest/
import csv
import aiofiles
import gspread.utils

# from https://stackoverflow.com/questions/46827007/runtimeerror-this-event-loop-is-already-running-in-python
import nest_asyncio
nest_asyncio.apply()

from MSMainClass import MSMainClass
import asyncio
from aiogoogle import Aiogoogle
import aiohttp
import os
from google.oauth2.service_account import Credentials
import gspread_asyncio


class MSConnGSAsync(MSMainClass):
    """ google sheet asynchronous writer"""
    logger_name = "gsconnectorasync"
    dir_name = "config"
    data_dir_name = "data"
    config_file_name = "gs_main_config.json"
    gs_json_credentials_key = "gs_json_credentials"
    gs_scopes_key = "gs_scopes"
    config_data = None
    async_gc = None

    def __init__(self):
        super().__init__()
        self.load_conf_data()


    def load_conf_data(self) -> dict:
        import MSReadJsonAsync
        reader = MSReadJsonAsync.MSReadJsonAsync(self.dir_name, self.config_file_name)
        self.config_data = reader.get_config_json_data_sync()
        return self.config_data

    def get_credentials(self):
        local_path = os.path.dirname(__file__)
        credentials_file_name = self.config_data.get(self.gs_json_credentials_key)
        CREDENTIALS_FILE_PATH = os.path.join(local_path, self.dir_name, credentials_file_name)
        scopes = self.config_data.get(self.gs_scopes_key)
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE_PATH)
        # scoped_cred = credentials.with_scopes(scopes)
        scoped_cred = credentials.with_scopes(scopes)
        # print(f"{scopes=} \n {CREDENTIALS_FILE_PATH=}")
        return scoped_cred

    def create_gs_client_manager(self):
        # gc = gspread.authorize(credentials)
        self.async_gspread_client_manager = gspread_asyncio.AsyncioGspreadClientManager(self.get_credentials)

    async def create_gs_client_async(self) -> gspread_asyncio.AsyncioGspreadClient:
        self.create_gs_client_manager()
        self.async_gc = await self.async_gspread_client_manager.authorize()
        # print(type(self.async_gc))
        return self.async_gc


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSConnGSAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    print(asyncio.run(connect.create_gs_client_async()))
    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
