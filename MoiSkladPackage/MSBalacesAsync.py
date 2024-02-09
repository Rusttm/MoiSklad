import datetime

from MSMainClass import MSMainClass

import time
import asyncio
from datetime import datetime


class MSBalacesAsync(MSMainClass):
    """ gather balances in one jsonfile"""
    logger_name = "balances"
    main_key = "ms_balance"
    dir_name = "config"
    config_file_name = "ms_balances_config.json"
    config_data = None

    def __init__(self):
        super().__init__()

    async def load_conf_data(self) -> bool:
        import MSReadJsonAsync
        reader = MSReadJsonAsync.MSReadJsonAsync(self.dir_name, self.config_file_name)
        self.config_data = await reader.get_config_json_data_async()
        return True

    async def get_accounts_sum_async(self) -> dict:
        res_accounts = dict({'деньги на счетах': 0})
        try:
            import MSAccountSumAsync
            ini_dict = MSAccountSumAsync.MSAccountSumAsync()
            res_accounts['деньги на счетах'] = await ini_dict.get_account_summ_async()
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return res_accounts

    async def get_stocks_cost_async(self) -> dict:
        """ return sum of all stores without excluded"""
        res_costs = dict({'склад себестоимость': 0})
        await self.load_conf_data()
        try:
            import MSStoresSumAsync
            ini_dict = MSStoresSumAsync.MSStoresSumAsync()
            stores_dict = await ini_dict.get_stores_cost_dict_async()
            excluded_stores_list = list(self.config_data.values())
            for store_name, store_sum in stores_dict.items():
                if store_name not in excluded_stores_list:
                    res_costs['склад себестоимость'] = res_costs.get('склад себестоимость', 0) + int(store_sum)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stores data, error: {e}"
            self.logger.error(msg)
        return res_costs

    async def get_customers_groups_sum_async(self) -> dict:
        """ return dict of groups with balances {'другие': 710918, 'москваконтрагенты': 450593, 'поставщики': 2984930}"""
        cust_groups = dict({'другие': 0})
        try:
            import MSCustBalAsync
            ini_dict = MSCustBalAsync.MSCustBalAsync()
            cust_groups = await ini_dict.get_cust_groups_sum_async()
            cust_groups = {key: -value for key, value in cust_groups.items()}
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers group balances data, error: {e}"
            self.logger.error(msg)
        return cust_groups

    async def form_balance_dict_async(self) -> dict:
        result_dict = dict({"Дата": datetime.now().strftime("%d.%m.%y %H:%M")})
        balance_sum = int()
        accounts_money_sum = await self.get_accounts_sum_async()
        balance_sum += sum([int(value) for value in accounts_money_sum.values()])
        result_dict.update(accounts_money_sum)
        stocks_sum = await self.get_stocks_cost_async()
        balance_sum += sum([int(value) for value in stocks_sum.values()])
        result_dict.update(stocks_sum)
        cust_groups_bal = await self.get_customers_groups_sum_async()
        balance_sum += sum([int(value) for value in cust_groups_bal.values()])
        result_dict.update(cust_groups_bal)
        result_dict.update({"Итог": balance_sum})
        return result_dict


if __name__ == "__main__":
    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSBalacesAsync()
    print(asyncio.run(connect.form_balance_dict_async()))
    print(f"report done in {int(start_time-time.time())}sec at {time.strftime('%H:%M:%S', time.localtime())}")



