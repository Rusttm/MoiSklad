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


class MSExportGSAsync(MSMainClass):
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
        if not self.async_gc:
            try:
                import MSConnGSAsync
                self.async_gc = MSConnGSAsync.MSConnGSAsync().create_gs_client_async()
            except Exception as e:
                msg = f"{__class__.__name__} cant create async_gc, Error: \n {e}"
                self.logger.warning(msg)
                print(msg)
                return None
        return self.async_gc

    async def save_spreadsheet_csv_async(self, spread_sheet_id: str = None,
                                         spread_sheet: gspread_asyncio.AsyncioGspreadSpreadsheet = None):
        await self.create_gc_async()
        if spread_sheet or spread_sheet_id:
            if not spread_sheet_id: spread_sheet_id = spread_sheet.id
            binary_file_data = await self.async_gc.export(spread_sheet_id, format=gspread.utils.ExportFormat.CSV)
            print(f"{binary_file_data=}")
            # with open("test_csv_file", 'wb') as new_file:
            #     new_file.write(binary_file_data)
            file_name = spread_sheet.title + ".csv"
            file_path = os.path.join(self.data_dir_name, file_name)
            async with aiofiles.open(file_path, 'wb') as ff:
                await ff.write(binary_file_data)
            return file_path
        else:
            msg = f"{__class__.__name__} cant convert to csv, "
            self.logger.warning(msg)
            print(msg)
            return None

    async def save_spreadsheet_xlsx_async(self, spread_sheet_id: str = None,
                                          spread_sheet: gspread_asyncio.AsyncioGspreadSpreadsheet = None):
        await self.create_gc_async()
        if spread_sheet or spread_sheet_id:
            if not spread_sheet_id: spread_sheet_id = spread_sheet.id
            binary_file_data = await self.async_gc.export(spread_sheet_id, format=gspread.utils.ExportFormat.EXCEL)
            print(f"{binary_file_data=}")
            file_name = spread_sheet.title + ".xlsx"
            file_path = os.path.join(self.data_dir_name, file_name)
            async with aiofiles.open(file_path, 'wb') as ff:
                await ff.write(binary_file_data)
            return file_path
        else:
            msg = f"{__class__.__name__} cant convert to xlsx"
            self.logger.warning(msg)
            print(msg)
            return None


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSExportGSAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    print(asyncio.run(connect.save_spreadsheet_csv_async()))
    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(start_time - time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")
