# -*- coding: utf-8 -*-
# from https://gspread-asyncio.readthedocs.io/en/latest/
from .GSConnAsync import GSConnAsync
import asyncio
import os
# from https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python
# its hide pandas deprecation information
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd

class GSMSContAsync(GSConnAsync):
    """ data handler """
    logger_name = f"{os.path.basename(__file__)}"
    ss_names_key = "gs_names"

    def __init__(self):
        super().__init__()

    async def save_data_ms_gs_async(self, ms_data: dict, gs_tag: str, insert=True, ws_id=0) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            ss_id = self.config_data.get(self.ss_names_key).get(gs_tag)
            import GSMSDataHandlerAsync
            handler = GSMSDataHandlerAsync.GSMSDataHandlerAsync()
            df = await handler.convert_ms_dict_2df_async(ms_data=ms_data)
            spread_sheet = await self.async_gc.open_by_key(ss_id)
            work_sheet = await spread_sheet.get_worksheet_by_id(ws_id)
            # df = pd.DataFrame(await work_sheet.get_all_values())
            if insert:
                await work_sheet.clear()
                await work_sheet.insert_rows([df.columns.values.tolist()] + df.values.tolist())
            else:
                await work_sheet.append_rows(df.values.tolist())

        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return df

    async def save_balances_ms_gs_async(self, ms_data: dict, gs_tag="gs_balance", insert=False, ws_id=1349066460) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            ss_id = self.config_data.get(self.ss_names_key).get(gs_tag)
            from .GSMSDataHandlerAsync import GSMSDataHandlerAsync
            handler = GSMSDataHandlerAsync()
            df = await handler.convert_ms_dict_2df_async(ms_data=ms_data)
            spread_sheet = await self.async_gc.open_by_key(ss_id)
            work_sheet = await spread_sheet.get_worksheet_by_id(ws_id)
            # df = pd.DataFrame(await work_sheet.get_all_values())
            if insert:
                await work_sheet.clear()
                await work_sheet.insert_rows([df.columns.values.tolist()] + df.values.tolist())
            else:
                await work_sheet.append_rows(df.values.tolist())

        except Exception as e:
            msg = f"{__class__.__name__} cant get spreadsheet metadata, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return df



if __name__ == "__main__":
    import time

    start_time = time.time()
    ms_data = {'data': {
        'Дата': '11.02.24 16:17',
        'деньги на счетах': 1858546,
        'склад себестоимость': 31512481,
        'другие': 710918,
        'москваконтрагенты': 450593,
        'поставщики': 2984930,
        'новосибирскконтрагенты': 698376,
        'покупатели пфо': 0,
        'Итог': 38215844},
        'col_list':
            ['Дата',
             'Итог',
             'деньги на счетах',
             'склад себестоимость',
             'поставщики',
             'новосибирскконтрагенты',
             'москваконтрагенты',
             'покупатели пфо',
             'другие']}
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = GSMSContAsync()
    # print(asyncio.run(
    #     connect.get_spreadsheet_ws_names_list_async(spread_sheet_id="1YtCslaQVP06Mqxr4I2xYn3w62teS5qd6ndN_MEU_jeE")))
    print(asyncio.run(
        connect.save_data_ms_gs_async(ms_data=ms_data, gs_tag="gs_test", insert=True)))
    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")
