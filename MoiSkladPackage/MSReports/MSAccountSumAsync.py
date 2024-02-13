from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass
import asyncio
import os
class MSAccountSumAsync(MSMainClass):
    """ clas get accounts remains"""
    logger_name = f"{os.path.basename(__file__)}"
    url_key = "url_money"
    save_2file = False
    async_requester = None

    def __init__(self):
        super().__init__()
        from MoiSkladPackage.MSConnectors.MSRequesterAsync import MSRequesterAsync
        self.async_requester = MSRequesterAsync()

    async def get_account_summ_async(self) -> int:
        """this function gets sum of bank accounts remains"""
        account_bal = int()
        # get account sum
        try:
            acc_req = await self.async_requester.get_api_data_async(url_conf_key=self.url_key, to_file=self.save_2file)
            account_bal = int()
            for account in acc_req['rows'][1:]:
                account_bal += int(account['balance']/100)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return account_bal

    async def get_account_remains_async(self) -> dict:
        """this function gets sum of bank accounts remains"""
        accounts_bal = dict({'accounts_sum': 0, 'accounts': dict()})
        # get account sum
        try:
            acc_req = await self.async_requester.get_api_data_async(url_conf_key=self.url_key, to_file=self.save_2file)
            new_dict = dict()
            accounts_sum = int()
            for account_elem in acc_req['rows'][1:]:
                account_num = account_elem['account']['name']
                account_sum = account_elem['balance']/100
                new_dict[account_num] = int(account_sum)
                accounts_sum += int(account_sum)
            accounts_bal['accounts'] = dict(sorted(new_dict.items(), key=lambda x: x[1], reverse=True))
            accounts_bal['accounts_sum'] = accounts_sum
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return accounts_bal

    def get_account_remains_sync(self) -> dict:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.get_account_remains_async())
        # result = asyncio.run(self.get_config_json_data_async(file_name=file_name))
        return result


if __name__ == "__main__":
    connect = MSAccountSumAsync()
    print(asyncio.run(connect.get_account_summ_async()))
    connect.logger.debug("accounting class initialized")
