import asyncio
import os
from MSMainClass import MSMainClass
import datetime

class MSPaymentsAsync(MSMainClass):
    """return out_payments in period by purpose"""
    logger_name = f"{os.path.basename(__file__)}"
    _url_outpayments_list = "url_outpayments_list"
    _url_expence_items_list = "url_expence_items_list"
    # _config_dir = "config"
    # _config_file_name = "ms_balances_config.json"
    # _config_data = None
    # _module_conf_dir = "config"
    # _module_conf_file = "ms_profit_config.json"
    _to_file = False
    _unknown_purpose = "неизвестно"  # для неопределенных платежей
    async_requester = None


    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        import MSRequesterAsync
        self.async_requester = MSRequesterAsync.MSRequesterAsync()

    async def get_purposes_dict_async(self, to_file=False) -> dict:
        """ purposes dict {purpose_href: purpose_name}"""
        if to_file:
            self._to_file = to_file
        purposes_dict = dict()
        try:
            purposes_json = await self.async_requester.get_api_data_async(url_conf_key=self._url_expence_items_list, to_file=self._to_file)
            for purpose in purposes_json['rows']:
                purpose_href = purpose['meta']['href']
                purpose_name = purpose['name']
                purposes_dict[purpose_href] = purpose_name
        except Exception as e:
            msg = f"module {__class__.__name__} can't read expenses items data, error: {e}"
            self.logger.error(msg)
        return purposes_dict

    async def get_payments_purpose_dict_async(self, from_date=None, to_date=None, to_file=False) -> dict:
        """ return dict {purpose: payments_sum}"""
        if to_file:
            self._to_file = to_file
        if not from_date:
            from_date = '2024-01-01'
        if not to_date:
            to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        request_param_line = f"filter=moment>={from_date} 00:00:00&moment<={to_date} 23:00:00"

        payments_purpose_dict = dict()
        try:
            self.async_requester.set_api_param_line(request_param_line)
            out_payments_json = await self.async_requester.get_api_data_async(url_conf_key=self._url_outpayments_list, to_file=self._to_file)
            for payment in out_payments_json['rows']:
                purpose_href = payment['expenseItem']['meta']['href']
                payment_sum = payment['sum']/100
                payments_purpose_dict[purpose_href] = payments_purpose_dict.get(purpose_href, 0) + payment_sum
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers_list data, error: {e}"
            self.logger.error(msg)
        return payments_purpose_dict

    async def get_purpose_sum_dict_async(self, from_date=None, to_date=None, to_file=False) -> dict:
        """ returns dict {purpose_name: payments_sum}"""
        if to_file:
            self._to_file = to_file
        purpose_sum_dict = dict()
        try:
            purposes_dict = await self.get_purposes_dict_async()
            purpose_payments_sum_dict = await self.get_payments_purpose_dict_async(from_date=from_date, to_date=to_date, to_file=to_file)
            purpose_sum_dict = {purposes_dict.get(href, self._unknown_purpose): summ for href, summ in purpose_payments_sum_dict.items()}
        except Exception as e:
            msg = f"module {__class__.__name__} can't read departments_list data, error: {e}"
            self.logger.error(msg)
        return purpose_sum_dict
    async def get_current_month_purpose_sum_dict_async(self, to_file=False) -> dict:
        cur_month = datetime.datetime.now().month
        cur_year = datetime.datetime.now().year
        from_date = f"{cur_year}-{cur_month}-01"
        to_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        res_dict = await self.get_purpose_sum_dict_async(from_date=from_date, to_date=to_date, to_file=to_file)
        return res_dict

    async def get_last_month_purpose_sum_dict_async(self, to_file=False) -> dict:
        payouts_last_month_profit = dict()
        try:
            cur_month = datetime.datetime.now().month
            cur_year = datetime.datetime.now().year
            cur_month_first_day = datetime.datetime.strptime(f"{cur_year}-{cur_month}-01", "%Y-%m-%d")
            last_month_last_day = cur_month_first_day - datetime.timedelta(days=1)
            last_month_first_day = datetime.datetime.strptime(
                f"{last_month_last_day.year}-{last_month_last_day.month}-01", "%Y-%m-%d")
            from_date = last_month_first_day.strftime("%Y-%m-%d")
            to_date = last_month_last_day.strftime("%Y-%m-%d")
            payouts_last_month_profit = await self.get_purpose_sum_dict_async(from_date, to_date)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read purposes sum data, error: {e}"
            self.logger.error(msg)
        return payouts_last_month_profit

if __name__ == "__main__":
    connect = MSPaymentsAsync()
    # print(asyncio.run(connect.get_purposes_dict_async()))
    # print(asyncio.run(connect.get_payments_purpose_dict_async()))
    # print(asyncio.run(connect.get_purpose_sum_dict_async()))
    # print(asyncio.run(connect.get_current_month_purpose_sum_dict_async()))
    print(asyncio.run(connect.get_last_month_purpose_sum_dict_async()))
    connect.logger.debug("stock_all class initialized")