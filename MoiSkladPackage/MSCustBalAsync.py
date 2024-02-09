import asyncio

from MSMainClass import MSMainClass


class MSCustBalAsync(MSMainClass):
    """ clas get sum of stores"""
    logger_name = "custbalasync"
    url_customers_bal = "url_customers_bal"
    url_customers_list = "url_customers_list"
    async_requester = None
    to_file = False
    main_key = "ms_balance"
    customers_columns_key = "customers_bal_columns"
    excluded_groups_key = "excluded_groups"
    include_other_companies_key = "include_other_companies"
    dir_name = "config"
    config_file_name = "ms_balances_config.json"
    config_data = None

    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        import MSRequesterAsync
        self.async_requester = MSRequesterAsync.MSRequesterAsync()

        # print(self.config_data)

    async def load_conf_data(self) -> dict:
        import MSReadJsonAsync
        reader = MSReadJsonAsync.MSReadJsonAsync(dir_name=self.dir_name, file_name=self.config_file_name)
        result = await reader.get_config_json_data_async()
        return result

    async def get_customers_dict_async(self):
        customers_dict = dict()
        try:
            self.async_requester.set_config(self.url_customers_list)
            to_file = self.to_file
            customers_json = await self.async_requester.get_api_data_async(to_file=to_file)
            for customer in customers_json['rows']:
                # customer_name = customer['name']
                customer_href = customer['meta']['href']
                customer_groups_list = customer['tags']
                customers_dict[customer_href] = customer_groups_list
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers_list data, error: {e}"
            self.logger.error(msg)
        return customers_dict

    async def get_customers_bal_async(self) -> dict:
        """this return dict {"position_href": cost}"""
        customers_bal = dict()
        try:
            self.async_requester.set_config(self.url_customers_bal)
            self.async_requester.set_api_param_line('filter=balance!=0')
            to_file = self.to_file
            cust_bal_dict = await self.async_requester.get_api_data_async(to_file=to_file)
            for customer in cust_bal_dict['rows']:
                customer_name = customer['counterparty']['name']
                customer_bal = customer['balance'] / 100
                customer_href = customer['counterparty']['meta']['href']
                customers_bal[customer_href] = [customer_bal, customer_name]
        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return customers_bal

    async def get_cust_groups_sum_async(self) -> dict:
        cust_groups_sum = dict()
        try:
            self.config_data =  await self.load_conf_data()
            customers_groups = await self.get_customers_dict_async()
            customers_bal = await self.get_customers_bal_async()
            customers_show_groups = self.config_data[self.main_key][self.customers_columns_key]
            customers_inc_excluded_groups = self.config_data[self.main_key][self.include_other_companies_key]
            other_customers = list(customers_inc_excluded_groups.values())
            for customer_href in customers_bal:
                customer_in_groups = customers_groups.get(customer_href, None)
                customer_bal = customers_bal.get(customer_href)[0]
                customer_name = customers_bal.get(customer_href)[1]
                if customer_in_groups:
                    for show_group in list(customers_show_groups):
                        customer_groups = customers_groups.get(customer_href)
                        if show_group in customer_groups:
                            cust_groups_sum[show_group] = cust_groups_sum.get(show_group, 0) + int(customer_bal)
                            break
                        elif customer_name in other_customers:
                            cust_groups_sum['другие'] = cust_groups_sum.get('другие', 0) + int(customer_bal)
                            break

        except Exception as e:
            msg = f"module {__class__.__name__} can't make cust_groups_sum data, error: {e}"
            self.logger.error(msg)
        return cust_groups_sum


if __name__ == "__main__":
    connect = MSCustBalAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    # print(asyncio.run(connect.get_customers_dict_async()))
    # print(asyncio.run(connect.get_customers_bal_async()))
    print(asyncio.run(connect.get_cust_groups_sum_async()))
    connect.logger.debug("stock_all class initialized")
