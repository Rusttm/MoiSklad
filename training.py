# -*- coding: utf8 -*-
import xlsxwriter
import datetime
import configparser
from pathlib import Path
import os
import ssl
import certifi
from datetime import datetime
from datetime import date
from scrapy import cmdline
from Scraping import run_scrapy
import requests
import json
import reports

def ini_file_write(file_name='bot.ini' , tree='MoiSklad', section='last_debt_file', entry='alex_debt_2021-02-17.xlsx'):
    try:
        ini_file = Path(file_name)
        config = configparser.ConfigParser()
        config.read(ini_file)
        config.set(tree, section, entry)
        config.write(ini_file.open("w"))
    except:
        print('ini file hasnt updated')


ini_file_write('bot.ini', 'MoiSklad', 'last_debt_file', 'alex_debt_2021-02-17.xlsx')
ini_file_write('alex.ini', 'MoiSklad', 'last_debt_file', 'alex_debt_2021-02-17.xlsx')

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)


# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Text with formatting.
#worksheet.write('A2', 'World', bold)

# Iterate over the data and write it out row by row.
for i in range(2):
    for item, cost in (expenses):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        if row!=4: worksheet.set_row(row, None, None, {'level': 2}) #choose a level for grouping and skip one
        row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total', bold)
worksheet.write(row, 1, f'=SUM(B1:B{row})', bold)

workbook.close()


def fill_the_df(data_linked):
    try:
        columns_for_df = ['Дата формирования отчета', 'Группы покупателя', 'Покупатель', 'Номер и дата отгрузки',
                          'ссылка на документ', 'Отсрочка, дней', 'Дней до оплаты', 'Размер просроченной задолженности', 'Статус']
        '''write to excell'''
        data_linked=sorted(data_linked, key=lambda y: (y[1], y[2], y[3])) #sorting by group and name
        try:
            today = date.today()
            sheet_name = str(today.strftime("%m-%d-%y"))
            alex_workbook = xlsxwriter.Workbook('alex_debt_%s.xlsx' % today)
            alex_worksheet = alex_workbook.add_worksheet(str(today.strftime("%m-%d-%y")))
            bold = alex_workbook.add_format({'bold': True})

            # insert top line
            for col_num, col_data in enumerate(columns_for_df):
                alex_worksheet.write(0, col_num, col_data, bold)

            customer_name ='Покупатель'
            new_customer_name =' '
            start_row = 1
            shift_row = 1 #shifting for write total sum

            #insert data
            for row_num, row_data in enumerate(data_linked):

                new_customer_name=row_data[2]

                if not ((customer_name == new_customer_name) or (customer_name =='Покупатель')):
                    alex_worksheet.set_row(row_num + shift_row, None, None, {'level': 0})
                    alex_worksheet.write(row_num + shift_row, 0, customer_name, bold)
                    alex_worksheet.write(row_num + shift_row, 6, 'Всего', bold)
                    alex_worksheet.write(row_num+ shift_row, 7, f'=SUM(H{start_row}:H{row_num+ shift_row})', bold)
                    shift_row += 1
                    start_row = row_num + shift_row + 1
                alex_worksheet.set_row(row_num + shift_row, None, None, {'level': 1})
                for col_num, col_data in enumerate(row_data):
                    alex_worksheet.write(row_num + shift_row, col_num, col_data)

                customer_name = new_customer_name





            alex_workbook.close()
        except Exception:
            print('Error, cant create file', Exception)

    except Exception:
        print('Error cant fill the DataFrame', Exception)


#fill_the_df(data_linked)
def test_module():
    new_sheet_name = '3a'
    shift = 1
    got_list=['1a','3a','3a+1','3a_1','5a']
    while new_sheet_name in got_list:
        new_sheet_name = f"{new_sheet_name}_{shift}"
        shift += 1
    return new_sheet_name

def test_module2():
    return ['1skghspkghd;lfgka','3a','3a+1','3a_1','5aadhsdfkljh sdkljfh']

today = date.today()
today_date = str(today.strftime("%d.%m.%y_%H:%M"))
today_date_req = str(today.strftime("%Y-%m-%d"))


def start_scrapy():
    cmdline.execute("scrapy runspider scrapy_lib.py".split())  # followall is the spider name
    return True


def xlsx_writer_train():
    workbook = xlsxwriter.Workbook('pfo_report.xlsx')
    worksheet = workbook.add_worksheet('temporary1')
    col= 0
    for row, data in enumerate(data_linked):
        worksheet.write_row(row, col, data)
    workbook.close()


print(datetime.now().month)
reports.monthly_report()