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


class MSConnGSAsync(MSMainClass):
    """ google sheet asynchronous writer"""
    logger_name = "requesterasync"
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
        self.create_gs_client_manager()

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

    async def create_gsheet_and_full_permission(self,
                                                spread_sheet_name=None) -> gspread_asyncio.AsyncioGspreadSpreadsheet:
        """ create new sheet, give full access permission and return obj spread_sheet"""
        if not spread_sheet_name: spread_sheet_name = "Test spread sheet"
        self.async_gc = await self.async_gspread_client_manager.authorize()
        spread_sheet = await self.async_gc.create(spread_sheet_name)
        spread_sheet_href = f"https://docs.google.com/spreadsheets/d/{spread_sheet.id}"
        # Allow anyone with the URL to write to this spreadsheet.
        await self.async_gc.insert_permission(spread_sheet.id, None, perm_type="anyone", role="writer")
        # print(f"{type(spread_sheet)=}") # <class 'gspread_asyncio.AsyncioGspreadSpreadsheet'>
        return spread_sheet

    async def add_worksheet_2spreadsheet(self, spread_sheet=None, work_sheet_name=None) -> object:
        if spread_sheet:
            self.async_gc = await self.async_gspread_client_manager.authorize()
            if not work_sheet_name: work_sheet_name = "Test sheet"
            work_sheet = await spread_sheet.add_worksheet(work_sheet_name, 10, 5)
            return work_sheet
        else:
            print(f"Не указан spread_sheet для добавления листа")
            return None

    async def save_spreadsheet_csv_async(self, spread_sheet: gspread_asyncio.AsyncioGspreadSpreadsheet = None,
                                         spread_sheet_id: str = None):
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

    async def save_spreadsheet_xlsx_async(self, spread_sheet: gspread_asyncio.AsyncioGspreadSpreadsheet = None,
                                          spread_sheet_id: str = None):
        # spread_sheet = await self.create_gsheet_and_full_permission()
        # zero_work_sheet = await spread_sheet.get_worksheet(0)
        # for row in range(1, 10):
        #     for col in range(1, 10):
        #         await zero_work_sheet.update_cell(row, col, str(col + row))
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
    connect = MSConnGSAsync()
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(self.get_api_data_async(to_file=to_file))
    # print(connect.load_conf_data())
    print(asyncio.run(connect.save_spreadsheet_csv_async()))
    # ws = asyncio.run(connect.add_worksheet_2spreadsheet(spread_sheet=ss))
    # print(ws)
    print(f"report done in {int(start_time - time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")
