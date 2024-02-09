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


class MSCreateGSAsync(MSMainClass):
    """ google sheet asynchronous writer"""
    logger_name = "gscreateasync"
    async_gc = None

    def __init__(self, async_gspread_client: gspread_asyncio.AsyncioGspreadClient = None):
        super().__init__()
        if async_gspread_client:
            self.async_gc = async_gspread_client

    async def create_gc_async(self):
        if not self.async_gc:
            try:
                import MSConnGSAsync
                print(f"")
                connector = MSConnGSAsync.MSConnGSAsync()
                self.async_gc = await connector.create_gs_client_async()
            except Exception as e:
                msg = f"{__class__.__name__} cant create async_gc, Error: \n {e}"
                self.logger.warning(msg)
                print(msg)
                return None
        return self.async_gc

    async def create_gsheet_and_full_permission(self,
                                                spread_sheet_name=None) -> gspread_asyncio.AsyncioGspreadSpreadsheet:
        """ create new sheet, give full access permission and return obj spread_sheet"""
        try:
            await self.create_gc_async()
            if not spread_sheet_name: spread_sheet_name = "Test spread sheet"
            spread_sheet = await self.async_gc.create(spread_sheet_name)
            spread_sheet_href = f"https://docs.google.com/spreadsheets/d/{spread_sheet.id}"
            # Allow anyone with the URL to write to this spreadsheet.
            await self.async_gc.insert_permission(spread_sheet.id, None, perm_type="anyone", role="writer")
            # print(f"{type(spread_sheet)=}") # <class 'gspread_asyncio.AsyncioGspreadSpreadsheet'>
            msg = f"created spreadsheet {spread_sheet_href}"
            print(msg)
            self.logger.info(msg)
            return spread_sheet
        except Exception as e:
            msg = f"{__class__.__name__} cant create google spread sheet {spread_sheet_name=}, Error: \n {e}"
            self.logger.warning(msg)
            return None

    async def add_worksheet_2spreadsheet(self, spread_sheet_id=None, spread_sheet_name=None, spread_sheet=None, work_sheet_name=None) -> object:
        try:
            await self.create_gc_async()
            if spread_sheet_id:
                spread_sheet = await self.async_gc.open_by_key(spread_sheet_id)
            elif spread_sheet_name:
                spread_sheet = await self.async_gc.open(spread_sheet_name)
            if spread_sheet:
                if not work_sheet_name: work_sheet_name = "Test sheet"
                work_sheet = await spread_sheet.add_worksheet(work_sheet_name, 10, 15)
                return work_sheet
            else:
                print(f"Не указан spread_sheet для добавления листа")
                return None
        except Exception as e:
            msg = f"{__class__.__name__} cant add worksheet to {spread_sheet_id=}, {spread_sheet_name=}, Error: \n {e}"
            self.logger.error(msg)
            return None



if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSCreateGSAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    # print(asyncio.run(connect.create_gsheet_and_full_permission(spread_sheet_name="Temporary spreadsheet")))
    print(asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                                         work_sheet_name="My new sheet")))
    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(start_time - time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")
