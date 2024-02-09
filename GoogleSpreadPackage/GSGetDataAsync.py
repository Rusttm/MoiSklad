# -*- coding: utf-8 -*-
import os

from GSMainClass import GSMainClass
import asyncio
import gspread_asyncio
# from https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd


class GSGetDataAsync(GSMainClass):
    """ google sheet asynchronous writer"""
    logger_name = f"{os.path.basename(__file__)}"
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
                import GSConnAsync
                connector = GSConnAsync.GSConnAsync()
                self.async_gc = await connector.create_gs_client_async()
            except Exception as e:
                msg = f"{__class__.__name__} cant create async_gc, Error: \n {e}"
                self.logger.warning(msg)
                print(msg)
                return None
        return self.async_gc

    async def get_ws_data_in_range_async(self, spread_sheet_id: str, ws_name: str, cells_range: tuple) -> pd.DataFrame:
        """ return values from sheet in range (A1, C5)"""
        try:
            import GSGetInfoAsync
            connector = GSGetInfoAsync.GSGetInfoAsync()
            name_is_in_ws = await connector.check_ws_name_is_exist(spread_sheet_id, ws_name)
            if not name_is_in_ws: raise AttributeError
            range_str = f"{ws_name}!{cells_range[0]}:{cells_range[1]}"
            await self.create_gc_async()
            spread_sheet = await self.async_gc.open_by_key(spread_sheet_id)
            ws_data = await spread_sheet.values_get(
                range_str)  # dict {'majorDimension': 'ROWS', 'range': "'My new sheet'!A1:C5", 'values': [[], ['1', '2'], ['', '34'], ['', '5'], ['4', '8', '9']]}
        except AttributeError:
            msg = f"{__class__.__name__} worksheet {ws_name} not in spreadsheet {spread_sheet_id} "
            self.logger.warning(msg)
            print(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet lists metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        else:
            # df = pd.DataFrame(ws_data.get("values"))
            values_list = ws_data.get("values")
            df = pd.DataFrame(values_list[1:], columns=values_list[0])
            return df
        return None

    async def get_all_ws_data_async(self, spread_sheet_id: str, ws_name: str) -> pd.DataFrame:
        """ return values from sheet in range (A1, C5)"""
        try:
            import GSGetInfoAsync
            connector = GSGetInfoAsync.GSGetInfoAsync()
            name_is_in_ws = await connector.check_ws_name_is_exist(spread_sheet_id, ws_name)
            if not name_is_in_ws: raise NameError
            ws_id = await connector.get_ws_id_by_name_async(spread_sheet_id, ws_name)
            await self.create_gc_async()
            spread_sheet = await self.async_gc.open_by_key(spread_sheet_id)
            work_sheet = await spread_sheet.get_worksheet_by_id(ws_id)
            ws_data = await work_sheet.get_all_values()
            # dict {'majorDimension': 'ROWS', 'range': "'My new sheet'!A1:C5", 'values': [[], ['1', '2'], ['', '34'], ['', '5'], ['4', '8', '9']]}
        except NameError:
            msg = f"{__class__.__name__} worksheet {ws_name} not in spreadsheet {spread_sheet_id} "
            self.logger.warning(msg)
            print(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet lists metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        else:
            df = pd.DataFrame(ws_data)
            return df
        return None


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSGetDataAsync()
    # print(asyncio.run(
    #     connect.get_ws_data_in_range_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
    #                                        ws_name="My new sheet",
    #                                        cells_range=("A1", "C5"))))
    print(asyncio.run(
        connect.get_all_ws_data_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                           ws_name="My new sheet")))

    print(f"report done in {int(time.time() - start_time )}sec at {time.strftime('%H:%M:%S', time.localtime())}")
