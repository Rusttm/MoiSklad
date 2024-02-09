# -*- coding: utf-8 -*-
from MSMainClass import MSMainClass
import asyncio
import gspread_asyncio
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd


class MSGetDataGSAsync(MSMainClass):
    """ google sheet asynchronous writer"""
    logger_name = "gsexporter"
    dir_name = "../MoiSkladPackage/config"
    data_dir_name = "../MoiSkladPackage/data"
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

    async def get_ws_data_range_async(self, spread_sheet_id: str, ws_name: str, cells_range: tuple) -> pd.DataFrame:
        """ return values from sheet in range (A1, C5)"""
        ws_data = list()
        try:
            import MSGetInfoGSAsync
            connector = MSGetInfoGSAsync.MSGetInfoGSAsync()
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


if __name__ == "__main__":
    import time

    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSGetDataGSAsync()
    print(asyncio.run(
        connect.get_ws_data_range_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE",
                                        ws_name="My new sheet",
                                        cells_range=("A1", "C5"))))

    print(f"report done in {int(time.time() - start_time )}sec at {time.strftime('%H:%M:%S', time.localtime())}")
