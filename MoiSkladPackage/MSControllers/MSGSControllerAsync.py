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
            from MoiSkladPackage.MSReports.MSReportBalacesAsync import MSReportBalacesAsync
            connector = MSReportBalacesAsync()
            balances_data = await connector.get_balance_data_async()
            await self.save_data_ms_gs_async(balances_data, gs_tag="gs_balance", ws_id=1349066460)
            msg = f"{__class__.__name__} saves balance data to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant saves balance data to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return balances_data

    async def save_profit_gs_custom_async(self, from_date, to_date, report_type="custom") -> pd.DataFrame:
        """ saves profit ms data to google spread"""
        profit_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSReportProfitAsync import MSReportProfitAsync
            connector = MSReportProfitAsync()
            profit_data = await connector.get_handled_expenses(from_date=from_date, to_date=to_date,
                                                               report_type=report_type)
            await self.save_data_ms_gs_async(profit_data, gs_tag="gs_profit", ws_id=539265374)
            msg = f"{__class__.__name__} saves custom profit report to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant custom profit report to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return profit_data

    async def save_profit_gs_daily_async(self) -> pd.DataFrame:
        """ saves profit ms data to google spread"""
        profit_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSReportProfitAsync import MSReportProfitAsync
            connector = MSReportProfitAsync()
            profit_data = await connector.get_daily_profit_report_async()
            await self.save_data_ms_gs_async(profit_data, gs_tag="gs_profit", ws_id=539265374)
            msg = f"{__class__.__name__} saves daily profit report to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant saves daily profit repor to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return profit_data

    async def save_profit_gs_monthly_async(self, to_year: int, to_month: int) -> pd.DataFrame:
        """ saves profit ms data to google spread"""
        profit_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSReportProfitAsync import MSReportProfitAsync
            connector = MSReportProfitAsync()
            profit_data = await connector.get_monthly_profit_report_async(to_year=to_year, to_month=to_month)
            await self.save_data_ms_gs_async(profit_data, gs_tag="gs_profit", ws_id=539265374)
            msg = f"{__class__.__name__} saves monthly profit report to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant save monthly profit report to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return profit_data

    async def save_daily_accounts_gs_async(self) -> pd.DataFrame:
        """ saves profit ms data to google spread"""
        accounts_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSAccountSumAsync import MSAccountSumAsync
            connector = MSAccountSumAsync()
            accounts_data = await connector.get_account_remains_async()
            gs_id = accounts_data.get("info").get("gs_id")
            ws_id = accounts_data.get("info").get("gs_ws_id")
            await self.save_data_ms_gs_id_async(accounts_data, gs_id=gs_id, ws_id=ws_id, time_col=True, insert=False)
            msg = f"{__class__.__name__} saves accounts report to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant accounts report to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return accounts_data

    async def save_daily_margins_gs_async(self) -> pd.DataFrame:
        """ saves profit ms data to google spread"""
        req_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSReportLowMarginAsync import MSReportLowMarginAsync
            connector = MSReportLowMarginAsync()
            req_data = await connector.get_today_low_margin_clients_async()
            gs_id = req_data.get("info").get("gs_id")
            ws_id = req_data.get("info").get("gs_ws_id")
            await self.save_data_ms_gs_id_async(req_data, gs_id=gs_id, ws_id=ws_id, time_col=True, insert=True)
            msg = f"{__class__.__name__} saves accounts report to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant accounts report to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return req_data

    async def save_daily_debt_gs_async(self) -> pd.DataFrame:
        """ saves ms data to google spread"""
        req_data = pd.DataFrame()
        try:
            from MoiSkladPackage.MSReports.MSReportDebtControlAsync import MSReportDebtControlAsync
            connector = MSReportDebtControlAsync()
            req_data = await connector.get_customers_debt_sum_async()
            gs_id = req_data.get("info").get("gs_id")
            ws_id = req_data.get("info").get("gs_ws_id")
            await self.save_data_ms_gs_id_async(req_data, gs_id=gs_id, ws_id=ws_id, time_col=True, insert=True)
            msg = f"{__class__.__name__} saves debt report to spreadsheet. "
            self.logger.debug(msg)
        except Exception as e:
            msg = f"{__class__.__name__} cant deebt report to spreadsheet, Error: \n {e} "
            self.logger.warning(msg)
            print(msg)
        return req_data


if __name__ == "__main__":
    controller = MSGSControllerAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    # print(asyncio.run(controller.save_balance_gs_async()))
    # print(asyncio.run(controller.save_profit_gs_custom_async(from_date="2023-01-01", to_date="2023-12-31")))
    # print(asyncio.run(controller.save_profit_gs_daily_async()))
    # print(asyncio.run(controller.save_profit_gs_monthly_async(to_year=2021, to_month=9)))
    # for year in range(2021,2024):
    #     for month in range(1,13):
    #         asyncio.run(controller.save_profit_gs_monthly_async(to_year=year, to_month=month))
    # print(asyncio.run(controller.save_daily_margins_gs_async()))
    print(asyncio.run(controller.save_daily_debt_gs_async()))
    # print(asyncio.run(controller.save_daily_accounts_gs_async()))
    controller.logger.debug("stock_all class initialized")

