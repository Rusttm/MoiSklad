from MSMainClass import MSMainClass

class MSBalaces(MSMainClass):
    """ gather balances in one jsonfile"""
    logger_name = "balances"
    ms_urls_key = "ms_urls"
    url_money = "url_money"
    excluded_stocks = ['Склад Гарантия', 'Склад Гарантия']
    excluded_groups = ['офис поставщики', 'банки', 'транспорт']
    cont_transport = ['ПАО "ТРАНСКОНТЕЙНЕР"', 'ФТС России', 'ООО "ТРАСКО"', 'ООО "МЕДИТЕРРАНЕАН ШИППИНГ КОМПАНИ РУСЬ"']
    customers_shape = ['поставщики', 'новосибирскконтрагенты', 'москваконтрагенты', 'покупатели пфо', 'транспорт',
                       'офис поставщики']

    def __init__(self):
        super().__init__()

    def get_accounts_sum(self) -> dict:
        res_accounts = dict({'accounts_sum': 0})
        try:
            import MSAccountSum
            ini_dict = MSAccountSum.MSAccountSum()
            res_accounts['accounts_sum'] = ini_dict.get_account_summ()
        except Exception as e:
            msg = f"module {__class__.__name__} can't read account data, error: {e}"
            self.logger.error(msg)
        return res_accounts
    # def get_accounts_sum(self):
    #     try:
    #         import MSConfigFile
    #         ini_dict = MSConfigFile.MSConfigFile()
    #         req_url = ini_dict.get_ini_json_file().get(self.ms_urls_key).get(self.url_key)
    #         header_for_token_auth = ini_dict.get_req_headers()
    #         import requests
    #         acc_req = requests.get(url=req_url, headers=header_for_token_auth)
    #     except Exception as e:
    #         print(e)



if __name__ == "__main__":
    connect = MSBalaces()
    print(connect.get_accounts_sum())
