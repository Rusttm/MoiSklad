import os

from GoogleSpreadPackage.GSMSContAsync import GSMSContAsync

import asyncio
import pandas as pd


class MSGSControllerAsync(GSMSContAsync):
    logger_name = f"{os.path.basename(__file__)}"
    def __init__(self):
        super().__init__()

    async def save_balance_gs_async(self) -> pd.DataFrame:
        """ saves balances ms data to google spread"""
        balances_data = pd.DataFrame()
        try:
            from MSBalacesAsync import MSBalacesAsync
            connector = MSBalacesAsync()
            balances_data = await connector.get_balance_data_async()
            await self.save_balances_ms_gs_async(balances_data)
            msg = f"{__class__.__name__} saves balance data to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant saves balance data to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return balances_data




if __name__ == "__main__":
    controller = MSGSControllerAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    print(asyncio.run(controller.save_balance_gs_async()))
    controller.logger.debug("stock_all class initialized")