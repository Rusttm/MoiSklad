# -*- coding: utf-8 -*-
# from https://gspread-asyncio.readthedocs.io/en/latest/
import csv
import aiofiles
import gspread.utils

from MSMainClass import MSMainClass
import asyncio
from aiogoogle import Aiogoogle
import aiohttp
import os
from google.oauth2.service_account import Credentials
import gspread_asyncio


class MSGetDataGSAsync(MSMainClass):
    """ google sheet asynchronous writer"""
    logger_name = "gsexporter"
    dir_name = "config"
    data_dir_name = "data"
    async_gc = None

    def __init__(self, async_gspread_client: gspread_asyncio.AsyncioGspreadClient = None):
        super().__init__()
        if async_gspread_client:
            self.async_gc = async_gspread_client

    async def create_gc_async(self):
        # asyncio.get_event_loop().close()
        if not self.async_gc:
            try:
                import MSConnGSAsync
                connector = MSConnGSAsync.MSConnGSAsync()
                self.async_gc = await connector.create_gs_client_async()
            except Exception as e:
                msg = f"{__class__.__name__} cant create async_gc, Error: \n {e}"
                self.logger.warning(msg)
                print(msg)
                return None
        return self.async_gc

    async def get_spreadsheet_metadata_async(self, spread_sheet_id: str) -> dict:
        spread_sheet_metadata = dict()
        try:
            await self.create_gc_async()
            spread_sheet = await self.async_gc.open_by_key(spread_sheet_id)
            spread_sheet_metadata = await spread_sheet.fetch_sheet_metadata()
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return spread_sheet_metadata

    async def get_spreadsheet_ws_names_async(self, spread_sheet_id: str) -> list:
        worksheets_metadata = list()

        try:
            await self.create_gc_async()
            spread_sheet = await self.async_gc.open_by_key(spread_sheet_id)
            spread_sheet_metadata = await spread_sheet.fetch_sheet_metadata()
            worksheets_metadata = dict(spread_sheet_metadata).get("sheets")
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet lists metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return worksheets_metadata


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSGetDataGSAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    # print(asyncio.run(connect.save_spreadsheet_csv_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    # print(
    #     asyncio.run(connect.get_spreadsheet_metadata_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    print(
        asyncio.run(
            connect.get_spreadsheet_ws_names_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))

    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(start_time - time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")
