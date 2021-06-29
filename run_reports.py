from datetime import datetime

# import sys
# sys.path.insert(0, '/home/rusttm/Desktop/moisklad/MoiSklad')

import sp_books
import finance

class report_forming():
    def __init__(self, answer):
        self.answer = answer
        self.type_report = answer['type_report']
        self.from_date =  answer['from_date']
        self.to_date =  answer['to_date']
        self.holder = answer['type_holder']

        self.formed_data = {'tag': '', 'result': ''}
        #print(answer['type_report'])

    def report_data(self):
        if self.answer['type_report'] == 'Sales taxbook':
            self.SalesBookReport()

        if self.answer['type_report'] == 'AccountSum':
            self.AccountSum()

        return self.formed_data
    #requested_report = {'type_report': answer['type_report'],
    #'from_date': answer['from_date'],
    #'to_date': answer['to_date'],}
    def AccountSum(self):
        self.formed_data['result'] = f'Acount balance on {str(datetime.now().strftime("%Y-%m-%d"))} is {str(round(finance.get_account_summ(), 2))} RUB.'
        print(self.formed_data)

    def SalesBookReport(self):
        try:
            self.mangement_report_link = sp_books.fill_the_sales_book(self.from_date, self.to_date)
            self.formed_data['tag'] = f'https://docs.google.com/spreadsheets/d/{str(self.mangement_report_link)}/edit#gid=0'
            self.formed_data['result'] = f'Sales taxbook report from {self.from_date} to {self.to_date} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'

        except:
            self.formed_data['result'] = "Error in SalesBookReport"

        print(self.formed_data)
