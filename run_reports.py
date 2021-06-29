from datetime import datetime

# import sys
# sys.path.insert(0, '/home/rusttm/Desktop/moisklad/MoiSklad')

import sp_books
import finance
import reports
import agents

class report_forming():
    def __init__(self, answer):
        self.answer = answer
        self.type_report = answer['type_report']
        self.from_date =  answer['from_date']
        self.to_date =  answer['to_date']
        self.holder = answer['type_holder']
        self.report_link = ''
        self.formed_data = {'tag': '', 'result': ''}
        #print(answer['type_report'])

    def report_data(self):
        if self.answer['from_date'] > self.answer['to_date']:
            self.formed_data['result'] = 'Error due to "Date from" > "Date to"'
            return self.formed_data

        if self.answer['type_report'] == 'Sales taxbook':
            self.SalesBookReport()

        if self.answer['type_report'] == 'Purchases taxbook':
            self.PurchasesBookReport()

        if self.answer['type_report'] == 'Profit report':
            self.MangementReport()

        if self.answer['type_report'] == 'Agents report':
            if self.answer['type_holder'] == 'Nsk':
                self.AgentNskReport()
            elif self.answer['type_holder'] == 'Pfo':
                self.AgentPfoReport()
            else:
                self.formed_data['result'] = 'Please choose an agent'

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
            self.report_link = sp_books.fill_the_sales_book(self.from_date, self.to_date)
            self.formed_data['tag'] = f'https://docs.google.com/spreadsheets/d/{str(self.report_link)}/edit#gid=0'
            self.formed_data['result'] = f'Sales taxbook report from {self.from_date} to {self.to_date} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
        except:
            self.formed_data['result'] = "Error in SalesBookReport"
        print(self.formed_data)

    def PurchasesBookReport(self):
        try:
            self.self.report_link = sp_books.fill_the_purchases_book(self.from_date, self.to_date)
            self.formed_data['tag'] = f'https://docs.google.com/spreadsheets/d/{str(self.report_link)}/edit#gid=0'
            self.formed_data['result'] = f'Purchases taxbook report from {self.from_date} to {self.to_date} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
        except:
            self.formed_data['result'] = "Error in PurchasesBookReport"
        print(self.formed_data)

    def MangementReport(self):
        try:
            self.report_link = reports.monthly_report(self.from_date, self.to_date)
            self.formed_data['tag'] = f'https://docs.google.com/spreadsheets/d/{str(self.report_link)}/edit#gid=0'
            self.formed_data['result'] = f'Profit report from {self.from_date} to {self.to_date} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
        except:
            self.formed_data['result'] = "Error in MangementReport"
        print(self.formed_data)

    def AgentNskReport(self):
        try:
            self.report_link = agents.get_nsk_agent_report(self.from_date, self.to_date)
            self.formed_data['tag'] = f'https://docs.google.com/spreadsheets/d/{str(self.report_link)}/edit#gid=0'
            self.formed_data['result'] = f'NSK agent report from {self.from_date} to {self.to_date} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
        except:
            self.formed_data['result'] = "Error in AgentNskReport"
        print(self.formed_data)

    def AgentPfoReport(self):
        try:
            self.report_link = agents.get_pfo_agent_report(self.from_date, self.to_date)
            self.formed_data['tag'] = f'https://docs.google.com/spreadsheets/d/{str(self.report_link)}/edit#gid=0'
            self.formed_data['result'] = f'PFO agent report from {self.from_date} to {self.to_date} was formed {str(datetime.now().strftime("%Y-%m-%d"))}!'
        except:
            self.formed_data['result'] = "Error in AgentPfoReport"
        print(self.formed_data)
