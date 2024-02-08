from MSMainClass import MSMainClass

class MSBalacesAsync(MSMainClass):
    """ gather balances in one jsonfile"""
    logger_name = "balances"
    main_key = "ms_balance"
    dir_name = "config"
    config_file_name = "ms_balances_config.json"
    config_data = None


    def __init__(self):
        super().__init__()
        self.config_data = self.load_conf_data()

    async def load_conf_data(self) -> dict:
        import MSReadJsonAsync
        reader = MSReadJsonAsync.MSReadJsonAsync(self.dir_name, self.config_file_name)
        return await reader.get_config_json_data_async()

    async def get_accounts_sum_async(self) -> dict:
        res_accounts = dict({'accounts_sum': 0})
        try:
            import MSAccountSumAsync
            ini_dict = MSAccountSumAsync.MSAccountSumAsync()
            res_accounts['accounts_sum'] = await ini_dict.get_account_summ_async()
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return res_accounts

    async def get_stocks_cost_async(self) -> dict:
        """ return sum of all stores without excluded"""
        res_costs = dict({'stores_sum': 0})
        try:
            import MSStoresSum
            ini_dict = MSStoresSum.MSStoresSum()
            stores_dict = ini_dict.get_stores_cost_dict()
            excluded_stores_list = list(self.config_data.values())
            for store_name, store_sum in stores_dict.items():
                if store_name not in excluded_stores_list:
                    res_costs['stores_sum'] = res_costs.get('stores_sum', 0) + int(store_sum)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stores data, error: {e}"
            self.logger.error(msg)
        return res_costs

    async def get_customers_balances_async(self):
        return False

if __name__ == "__main__":
    connect = MSBalacesAsync()
    print(connect.get_stocks_cost_async())
