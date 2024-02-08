from MSMainClass import MSMainClass


class MSStoresSum(MSMainClass):
    """ clas get sum of stores"""
    logger_name = "stores"
    ms_urls_key = "ms_urls"
    url_key = "url_stores"

    def __init__(self):
        super().__init__()

    def get_stores_good_price(self) -> int:
        """this function gets sum of stores remains"""
        account_bal = int()
        # get account sum
        try:
            import MSConfigFile
            ini_dict = MSConfigFile.MSConfigFile()
            req_url = ini_dict.get_ini_json_file().get(self.ms_urls_key).get(self.url_key)
            header_for_token_auth = ini_dict.get_req_headers()
            import requests
            acc_req = requests.get(url=req_url, headers=header_for_token_auth)
            # with open('money_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            account_bal = int()
            for account in acc_req.json()['rows']:
                account_bal += int(account['balance']/100)
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return account_bal

    def get_account_remains(self) -> dict:
        """this function gets sum of bank accounts remains"""
        accounts_bal = dict({'accounts_sum': 0, 'accounts': dict()})
        # get account sum
        try:
            import MSConfigFile
            ini_dict = MSConfigFile.MSConfigFile()
            req_url = ini_dict.get_ini_json_file().get(self.ms_urls_key).get(self.url_key)
            header_for_token_auth = ini_dict.get_req_headers()
            import requests
            acc_req = requests.get(url=req_url, headers=header_for_token_auth)
            # with open('money_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            new_dict = dict()
            accounts_sum = int()
            for account_elem in acc_req.json()['rows'][1:]:
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


if __name__ == "__main__":
    connect = MSStoresSum()
    # print(connect.get_account_summ())
    print(connect.get_account_remains())
    connect.logger.debug("accounting class initialized")
