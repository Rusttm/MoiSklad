import asyncio

from MSMainClass import MSMainClass


class MSCustBalAsync(MSMainClass):
    """ clas get sum of stores"""
    logger_name = "stores"
    url_customers_bal = "url_customers_bal"
    url_customers_list = "url_customers_list"
    async_requester = None
    to_file = False

    def __init__(self, to_file=False):
        super().__init__()
        if to_file:
            self.to_file = to_file
        import MSRequesterAsync
        self.async_requester = MSRequesterAsync.MSRequesterAsync()

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
            to_file = self.to_file
            cust_bal_dict = await self.async_requester.get_api_data_async(to_file=to_file)
            for customer in cust_bal_dict['rows']:
                customer_name = customer['counterparty']['name']
                customer_bal = customer['balance'] / 100
                customer_href = customer['counterparty']['meta']['href']

        except Exception as e:
            msg = f"module {__class__.__name__} can't read stock_all data, error: {e}"
            self.logger.error(msg)
        return customers_bal


if __name__ == "__main__":
    connect = MSCustBalAsync()
    # print(connect.get_stores_good_price())
    # print(connect.get_stores_dict())
    print(asyncio.run(connect.get_customers_dict_async()))
    connect.logger.debug("stock_all class initialized")
