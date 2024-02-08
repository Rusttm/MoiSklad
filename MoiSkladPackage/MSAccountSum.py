from MSMainClass import MSMainClass


class MSAccountSum(MSMainClass):
    """ clas get accounts remains"""
    logger_name = "accounting"
    ms_urls_key = "ms_urls"
    url_key = "url_money"

    def __init__(self):
        super().__init__()

    def account_summ(self) -> int:
        """this function gets sum of bank accounts remains"""
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


if __name__ == "__main__":
    connect = MSAccountSum()
    print(connect.account_summ())
    connect.logger.debug("accounting class initialized")
