from MSMainClass import MSMainClass


class MSAccountSum(MSMainClass):
    logger_name = "accounting"

    def __init__(self):
        super().__init__()

    def account_summ(self):
        """'''this function gets bank account remains'''"""
        # get account sum
        try:
            acc_req = requests.get(url=url_money, headers=header_for_token_auth)
            # with open('money_req_list.json', 'w') as ff:
            #     json.dump(acc_req.json(), ff, ensure_ascii=False)
            for account in acc_req.json()['rows']:
                try:
                    acc_name = account['account']['name']
                    acc_courses = self.account_exch
                    if acc_name in acc_courses.keys():
                        self.account_bal += account['balance'] * acc_courses[acc_name] / 100
                    else:
                        self.account_bal += account['balance']/100
                except:
                    self.account_bal += account['balance'] / 100
        except IndexError:
            print('Cant read account data', Exception)
        #print(f'account_sum_ready')
        #print(self.account_bal)


if __name__ == "__main__":
    connect = MSAccountSum()
    connect.logger.debug("accounting class initialized")
