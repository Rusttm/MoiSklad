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
import requests
import json

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


data_linked=[['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 99 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=02631baa-6613-11eb-0a80-006c000ba223', 21, 7, 6610.94, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЕВРОТЕКС СТИЛЬ', '№ 71 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=0c84092f-6548-11eb-0a80-095b000a745f', 30, 9, 120621.42, 'В рамках отсрочки'], ['17.02.21', 'покупатели', 'ЭРА ч.л.', '№ 83 от 2021-01-28', 'https://online.moysklad.ru/app/#demand/edit?id=0d377794-66bd-11eb-0a80-018700056801', 0, -20, 17425.8, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 144 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=1336812d-7022-11eb-0a80-032000048430', 14, 13, 99125.76, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 351 от 2020-08-11', 'https://online.moysklad.ru/app/#demand/edit?id=1e832980-6533-11eb-0a80-046b00063f53', 0, -190, 28800.8, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 132 от 2021-02-12', 'https://online.moysklad.ru/app/#demand/edit?id=21493dec-6ce3-11eb-0a80-036100021a68', 21, 16, 5851.2, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 139 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=231f845c-7006-11eb-0a80-04e50002a652', 14, 13, 6475.0, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЕВРОТЕКС СТИЛЬ', '№ 72 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=29dfb18d-6548-11eb-0a80-03c0000a6d71', 30, 9, 571825.18, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "МТ-СИБИРЬ"', '№ 101 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=399be511-6613-11eb-0a80-06c5000bae7e', 14, 0, 27600.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 318 от 2020-07-29', 'https://online.moysklad.ru/app/#demand/edit?id=3bf93452-6532-11eb-0a80-03c00005e1bd', 0, -203, 24193.11, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "МТ-СИБИРЬ"', '№ 125 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=3c5469f7-6c4c-11eb-0a80-047c001a8498', 14, 8, 14000.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 116 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=3ed8a706-6abe-11eb-0a80-0067000a5ab6', 0, -8, 25411.5, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 74 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=3ef4d612-6549-11eb-0a80-02fb000a5f76', 21, 0, 145.5, 'В рамках отсрочки'], ['17.02.21', 'покупатели', 'ООО "ТРЕЙД-НСК"', '№ 86 от 2021-01-29', 'https://online.moysklad.ru/app/#demand/edit?id=45edbd61-654b-11eb-0a80-07f1000aa0ff', 30, 11, 12746.5, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 115 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=465ca1ed-6aa5-11eb-0a80-06da00056fc3', 0, -8, 23735.57, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 141 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=46e82a2d-701b-11eb-0a80-060800038de1', 21, 20, 246.68, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 360 от 2020-08-14', 'https://online.moysklad.ru/app/#demand/edit?id=49625a11-6533-11eb-0a80-03c000061465', 0, -187, 21976.34, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТАТСТРОЙКАМА"', '№ 710 от 2020-12-17', 'https://online.moysklad.ru/app/#demand/edit?id=51fcaba7-6530-11eb-0a80-016900053e5b', 14, -48, 6727.33, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 109 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=52804313-6a87-11eb-0a80-02d9000299be', 14, 6, 15688.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "СИБКЕДР"', '№ 124 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=56ab95c0-6c38-11eb-0a80-086b0016a127', 14, 8, 14069.66, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 102 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=5816fa8b-6654-11eb-0a80-021500016fe0', 30, 16, 22750.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 147 от 2021-02-17', 'https://online.moysklad.ru/app/#demand/edit?id=58be0543-70e0-11eb-0a80-024500014e24', 0, 0, 3961.67, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 8 от 2021-01-12', 'https://online.moysklad.ru/app/#demand/edit?id=5a320f8f-6534-11eb-0a80-046b0006833e', 14, -22, 41944.16, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 127 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=5cd75d2d-6c59-11eb-0a80-050f001cdf2e', 0, -6, 41817.0, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 133 от 2021-02-12', 'https://online.moysklad.ru/app/#demand/edit?id=5d0ef4a0-6ce8-11eb-0a80-0495000332b0', 21, 16, 992.31, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "АВРО"', '№ 358 от 2020-08-13', 'https://online.moysklad.ru/app/#demand/edit?id=64dc4edf-6515-11eb-0a80-03c0000176e4', 21, -167, 1463.98, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 87 от 2021-02-01', 'https://online.moysklad.ru/app/#demand/edit?id=68381e78-654b-11eb-0a80-03c0000b0582', 21, 5, 38160.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ЕВРОПЛАСТ-Ф"', '№ 148 от 2021-02-17', 'https://online.moysklad.ru/app/#demand/edit?id=6afd74a9-70ee-11eb-0a80-09050002d316', 21, 21, 110840.93, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "МТ-СИБИРЬ"', '№ 103 от 2021-02-04', 'https://online.moysklad.ru/app/#demand/edit?id=6b90cd1d-66f5-11eb-0a80-05e9000ffbb9', 14, 1, 4800.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели', 'Ульяновск ч\\л', '№ 62 от 2021-01-25', 'https://online.moysklad.ru/app/#demand/edit?id=6d94ab5e-66bd-11eb-0a80-06cc0005e71a', 0, -23, 260896.1, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "СИБИРСКИЙ ЛЕС"', '№ 341 от 2020-08-06', 'https://online.moysklad.ru/app/#demand/edit?id=7338e1a3-652e-11eb-0a80-07f10004e407', 14, -181, 13873.03, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ИП Сапогова Таисия Владимировна', '№ 136 от 2021-02-15', 'https://online.moysklad.ru/app/#demand/edit?id=77bed696-6f49-11eb-0a80-03610023352f', 0, -2, 2549.52, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ООО "БМ ГРУПП"', '№ 126 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=780be9b7-6c4f-11eb-0a80-034b001afca3', 0, -6, 65600.52, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 76 от 2021-01-28', 'https://online.moysklad.ru/app/#demand/edit?id=806b10a3-6549-11eb-0a80-0169000a3bf9', 21, 1, 1173.83, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 142 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=85628279-7021-11eb-0a80-09fb0004383c', 14, 13, 15688.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО ПКФ "МЕБЕЛЬНАЯ ФАБРИКА"', '№ 93 от 2021-02-03', 'https://online.moysklad.ru/app/#demand/edit?id=85f88009-6610-11eb-0a80-06c5000b13c2', 14, 0, 68720.76, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 377 от 2020-08-21', 'https://online.moysklad.ru/app/#demand/edit?id=87a0e491-6533-11eb-0a80-03c000061f86', 0, -180, 41003.32, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 69 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=88a66bc6-6548-11eb-0a80-07f10009fac4', 30, 9, 231224.97, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 48 от 2021-01-20', 'https://online.moysklad.ru/app/#demand/edit?id=893dcf75-6544-11eb-0a80-046b0009dd26', 30, 2, 46072.8, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 88 от 2021-02-01', 'https://online.moysklad.ru/app/#demand/edit?id=8fcd4294-654b-11eb-0a80-046b000b2df2', 21, 5, 14160.77, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТАРСК-НСК"', '№ 725 от 2020-12-23', 'https://online.moysklad.ru/app/#demand/edit?id=944aafbc-652f-11eb-0a80-095b00051ee3', 14, -42, 0.13000000000010914, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 118 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=96c68e3b-6ad3-11eb-0a80-0972000ed28a', 30, 22, 4823.0, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ИП Михеева Нина Владимировна', '№ 128 от 2021-02-11', 'https://online.moysklad.ru/app/#demand/edit?id=99fe9b80-6c59-11eb-0a80-006c001dbe09', 0, -6, 164513.3, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ДМЭЛ"', '№ 146 от 2021-02-17', 'https://online.moysklad.ru/app/#demand/edit?id=9e07f5c4-70c5-11eb-0a80-0098000082be', 7, 7, 22624.45, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'Балаян Артик Арамович', '№ 128 от 2020-03-18', 'https://online.moysklad.ru/app/#demand/edit?id=9e497913-6522-11eb-0a80-03c00002f2a4', 0, -336, 0.010000000009313226, 'Просрочено!'], ['17.02.21', 'покупатели', 'ООО "ТРЕЙД-НСК"', '№ 723 от 2020-12-23', 'https://online.moysklad.ru/app/#demand/edit?id=a0a140af-6645-11eb-0a80-09660000a1d7', 30, -26, 33141.94, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 59 от 2021-01-22', 'https://online.moysklad.ru/app/#demand/edit?id=a2a9807d-6546-11eb-0a80-07f10009a1f7', 30, 4, 82600.56, 'В рамках отсрочки'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 89 от 2021-02-01', 'https://online.moysklad.ru/app/#demand/edit?id=a567f0b5-654b-11eb-0a80-02fb000ac985', 30, 14, 114769.17, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 49 от 2021-01-20', 'https://online.moysklad.ru/app/#demand/edit?id=aff86963-6544-11eb-0a80-046b0009e350', 21, -7, 2162.09, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "СИБИРСКИЙ ЛЕС"', '№ 342 от 2020-08-06', 'https://online.moysklad.ru/app/#demand/edit?id=b2e18c43-652e-11eb-0a80-07f10004f00c', 14, -181, 4514.389999999999, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЭРА', '№ 60 от 2021-01-22', 'https://online.moysklad.ru/app/#demand/edit?id=b9269136-6546-11eb-0a80-06bd000a98e2', 30, 4, 11375.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 10 от 2021-01-12', 'https://online.moysklad.ru/app/#demand/edit?id=bc2cd42e-653c-11eb-0a80-01690007bce2', 14, -22, 1174.62, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "КРАСЛЕНТА"', '№ 31 от 2021-01-15', 'https://online.moysklad.ru/app/#demand/edit?id=bc8b68bc-653f-11eb-0a80-02fb00089407', 14, -19, 0.3999999999996362, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ИНТЕР-ТРЕЙД"', '№ 143 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=c056a4c0-7021-11eb-0a80-052c00043846', 14, 13, 1716.66, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 395 от 2020-08-28', 'https://online.moysklad.ru/app/#demand/edit?id=c3ee4d16-6533-11eb-0a80-046b00065f0d', 0, -173, 45532.89, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ПАЛЛЕТ СЕРВИС"', '№ 117 от 2021-02-09', 'https://online.moysklad.ru/app/#demand/edit?id=c79ea5c6-6acc-11eb-0a80-0865000d2da2', 14, 6, 10471.939999999999, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 41 от 2021-01-19', 'https://online.moysklad.ru/app/#demand/edit?id=d6e3c2e6-6542-11eb-0a80-01690008dbe8', 14, -15, 12000.0, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ИП Добровольская Жанна Александровна', '№ 145 от 2021-02-16', 'https://online.moysklad.ru/app/#demand/edit?id=dc0150dc-7058-11eb-0a80-0320000eccdb', 0, -1, 328482.52, 'Просрочено!'], ['17.02.21', 'москваконтрагенты', 'ЕВРОТЕКС СТИЛЬ', '№ 70 от 2021-01-27', 'https://online.moysklad.ru/app/#demand/edit?id=e08b22d5-6547-11eb-0a80-07f10009d6f1', 30, 9, 147009.0, 'В рамках отсрочки'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 121 от 2021-02-10', 'https://online.moysklad.ru/app/#demand/edit?id=e0dd1895-6b73-11eb-0a80-050f00056c8b', 21, 14, 301121.73, 'В рамках отсрочки'], ['17.02.21', 'покупатели пфо', 'ООО "ЕВРОПЛАСТ-Ф"', '№ 719 от 2020-12-22', 'https://online.moysklad.ru/app/#demand/edit?id=ec43307d-6527-11eb-0a80-095b0003a69c', 21, -36, 71293.92, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ЭЛДОРС"', '№ 24 от 2021-01-14', 'https://online.moysklad.ru/app/#demand/edit?id=ecbfbf4c-653e-11eb-0a80-095b0008ad8b', 14, -20, 5500.0, 'Просрочено!'], ['17.02.21', 'новосибирскконтрагенты', 'ООО "ТЕКСФОМ"', '№ 746 от 2020-12-28', 'https://online.moysklad.ru/app/#demand/edit?id=f13b06f5-6531-11eb-0a80-006700059dcf', 21, -30, 62737.16, 'Просрочено!'], ['17.02.21', 'покупатели пфо', 'ООО "ХОУМ МЕБЕЛЬ"', '№ 407 от 2020-09-02', 'https://online.moysklad.ru/app/#demand/edit?id=f9b1c658-6533-11eb-0a80-06bd00064569', 0, -168, 76876.5, 'Просрочено!']]


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


product_dict = {'https://online.moysklad.ru/api/remap/1.2/entity/product/cf791984-5779-11eb-0a80-06ec00b70a3a': 2562.4, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cf89eb5f-5779-11eb-0a80-06ec00b70a3e': 12814.7, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cf93d85d-5779-11eb-0a80-06ec00b70a4e': 349.4, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4ea177f2-576a-11eb-0a80-06ec00b50cd9': 3378.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cfa375ce-5779-11eb-0a80-06ec00b70a53': 1165.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4cb1ba97-576a-11eb-0a80-06ec00b50afa': 16355.5, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4cb3f720-576a-11eb-0a80-06ec00b50afe': 16355.5, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4cb6550d-576a-11eb-0a80-06ec00b50b02': 19562.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cbdf92f3-5779-11eb-0a80-06ec00b70579': 1070.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cbe1cc42-5779-11eb-0a80-06ec00b7057d': 1069.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4cd062d0-576a-11eb-0a80-06ec00b50b1c': 2145.5, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cd6d1c67-5779-11eb-0a80-06ec00b70768': 1060.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cda28a2d-5779-11eb-0a80-06ec00b707c5': 1482.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cdab4250-5779-11eb-0a80-06ec00b707d5': 27223.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cdadb697-5779-11eb-0a80-06ec00b707d9': 12076.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cdb55549-5779-11eb-0a80-06ec00b707e5': 314.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cdce0b75-5779-11eb-0a80-06ec00b7080e': 2964.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cea638a6-5779-11eb-0a80-06ec00b70966': 6249.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/1238b56c-6798-11eb-0a80-019900220df8': 5983.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cd8a356c-5779-11eb-0a80-06ec00b7079d': 27263.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cef5fb4f-5779-11eb-0a80-06ec00b709f7': 3707.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cf0d1402-5779-11eb-0a80-06ec00b70a1f': 1377.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/ce0c7bdd-5779-11eb-0a80-06ec00b70877': 2010.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/ce10734c-5779-11eb-0a80-06ec00b7087f': 2118.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/ce128e74-5779-11eb-0a80-06ec00b70883': 638.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/ce14f333-5779-11eb-0a80-06ec00b70887': 1482.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4cd92ec5-576a-11eb-0a80-06ec00b50b27': 128606.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4d0540d7-576a-11eb-0a80-06ec00b50b54': 179000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4cdc1014-576a-11eb-0a80-06ec00b50b2b': 22660.0, 'https://online.moysklad.ru/api/remap/1.2/entity/product/cd6520ae-5779-11eb-0a80-06ec00b7075c': 21234.5, 'https://online.moysklad.ru/api/remap/1.2/entity/product/4ebb73ea-576a-11eb-0a80-06ec00b50d01': 212841.5, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6acee48-576b-11eb-0a80-06ec00b52a80': 9266.91111111111, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6aec30d-576b-11eb-0a80-06ec00b52a84': 8258.333333333334, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6b084e0-576b-11eb-0a80-06ec00b52a88': 7444.136666666666, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6b4b395-576b-11eb-0a80-06ec00b52a90': 10969.753968253968, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6b676d5-576b-11eb-0a80-06ec00b52a94': 11693.611111111111, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6ba20c1-576b-11eb-0a80-06ec00b52a9c': 16949.584444444445, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6c3dee7-576b-11eb-0a80-06ec00b52ab0': 1158.779761904762, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6c6564c-576b-11eb-0a80-06ec00b52ab4': 641.8854166666666, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6e2de6c-576b-11eb-0a80-06ec00b52ad4': 1220.3072916666667, 'https://online.moysklad.ru/api/remap/1.2/entity/product/c6e536e6-576b-11eb-0a80-06ec00b52ad8': 1619.1846153846154}

demand_payed = {'https://online.moysklad.ru/api/remap/1.2/entity/demand/5c1b5f34-69ce-11eb-0a80-05f4002445e1': 2237982.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/58b3942a-6a93-11eb-0a80-02d90003028f': 1745130.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/868d3304-6a9d-11eb-0a80-04220003e325': 8997120.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/3325b4ae-6aa5-11eb-0a80-097200050f25': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/4a17859a-6adc-11eb-0a80-03400011914e': 8712900.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/c4563ee3-6539-11eb-0a80-02fb000766c4': 78000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/755213ce-6b45-11eb-0a80-02e90001fe2c': 2114240.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/f54efa18-654a-11eb-0a80-03c0000aed9e': 271949.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/ed78546e-6545-11eb-0a80-00670009c88d': 2097827.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/c130559e-654b-11eb-0a80-046b000b3654': 1908000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/2bb4bde7-6542-11eb-0a80-01690008bed3': 1372582.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/adf51ae3-6545-11eb-0a80-03c00009dc58': 487257.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/d085c5e3-6794-11eb-0a80-06d400080629': 6942309.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/12912fb7-6787-11eb-0a80-033800058929': 250000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/06a69f4e-6f51-11eb-0a80-04950025a769': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/def7b357-6525-11eb-0a80-006700033d69': 10698579, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/72b210d5-6525-11eb-0a80-046b00034085': 855000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/06c1382b-6f3b-11eb-0a80-07710023492d': 1650000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/d9d4adce-6536-11eb-0a80-01690006820b': 2866500.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/dc0150dc-7058-11eb-0a80-0320000eccdb': 5000000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/4a38557a-653c-11eb-0a80-05dc0007b9ac': 588000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/0f727b16-653f-11eb-0a80-095b0008b3d1': 588000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/5d35a4f5-6540-11eb-0a80-03c00008ed16': 1176000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/6df4201b-6c08-11eb-0a80-034b0013f0f5': 5000000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/de39cf2e-6541-11eb-0a80-05dc00090114': 8496398.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/8e20d685-71a1-11eb-0a80-00a500029ab2': 1470652.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/bd7c3b83-718b-11eb-0a80-053a00020cba': 653549.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/41d8e545-71a4-11eb-0a80-06190002b9c1': 2067000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/9e07f5c4-70c5-11eb-0a80-0098000082be': 2262445.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/51fcaba7-6530-11eb-0a80-016900053e5b': 672733.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/b9269136-6546-11eb-0a80-06bd000a98e2': 1137500.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/74c1500a-71a8-11eb-0a80-024f00033f6e': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/4d3b8809-71b0-11eb-0a80-024f0003d77d': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/893dcf75-6544-11eb-0a80-046b0009dd26': 4607280.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/ec43307d-6527-11eb-0a80-095b0003a69c': 7129392.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/a2a9807d-6546-11eb-0a80-07f10009a1f7': 8260056.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/f165456b-7737-11eb-0a80-07710002efe5': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/c16260f1-728b-11eb-0a80-03460005f966': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/5057539a-766c-11eb-0a80-083400409e95': 2544000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/399be511-6613-11eb-0a80-06c5000bae7e': 2760000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/85628279-7021-11eb-0a80-09fb0004383c': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/c056a4c0-7021-11eb-0a80-052c00043846': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/52804313-6a87-11eb-0a80-02d9000299be': 1568800.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/29dfb18d-6548-11eb-0a80-03c0000a6d71': 57182518, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/e08b22d5-6547-11eb-0a80-07f10009d6f1': 14700900, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/0c84092f-6548-11eb-0a80-095b000a745f': 12062142, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/266eef46-770f-11eb-0a80-00830000a6b9': 0.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/465ca1ed-6aa5-11eb-0a80-06da00056fc3': 2373557.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/5cd75d2d-6c59-11eb-0a80-050f001cdf2e': 4181700.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/3ed8a706-6abe-11eb-0a80-0067000a5ab6': 2541150.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/a567f0b5-654b-11eb-0a80-02fb000ac985': 11476917, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/88a66bc6-6548-11eb-0a80-07f10009fac4': 23122497, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/780be9b7-6c4f-11eb-0a80-034b001afca3': 3000000.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/68381e78-654b-11eb-0a80-03c0000b0582': 2314014.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/21493dec-6ce3-11eb-0a80-036100021a68': 585120.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/46e82a2d-701b-11eb-0a80-060800038de1': 24668.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/8fcd4294-654b-11eb-0a80-046b000b2df2': 1416077.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/02631baa-6613-11eb-0a80-006c000ba223': 661094.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/5d0ef4a0-6ce8-11eb-0a80-0495000332b0': 99231.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/c8710e08-726a-11eb-0a80-00ab000238d6': 216045.0, 'https://online.moysklad.ru/api/remap/1.2/entity/demand/a3836983-7afb-11eb-0a80-00670000bfdf': 22219581}

[['№ п/п', 'Дата отгрузки', 'Номер отгрузки', 'Наименование покупателя', 'Стоимость продажи', 'Себестоимость', 'Прибыль', 'Оплачено', 'Группа'], ['1', '2', '3', '4', '5', '6', '7', '8', '9'], [1, '08.02.21', '108', 'ООО "НВ-ГРУПП"', 22379.82, 11360.804807716371, 11019.015192283628, 22379.82, 'Саратов'], [2, '09.02.21', '110', 'ИП Исаев Дмитрий Викторович', 17451.3, 8548.562415458939, 8902.73758454106, 17451.3, 'Саратов'], [3, '09.02.21', '115', 'ИП Сапогова Таисия Владимировна', 23735.57, 13851.1069097951, 9884.4630902049, 23735.57, 'Саратов'], [4, '09.02.21', '116', 'ИП Сапогова Таисия Владимировна', 25411.5, 14991.59177749262, 10419.90822250738, 25411.5, 'Саратов'], [5, '11.02.21', '126', 'ООО "БМ ГРУПП"', 65600.52, 33587.907879754755, 32012.61212024525, 30000.0, 'Саратов'], [6, '11.02.21', '127', 'ИП Сапогова Таисия Владимировна', 41817.0, 26040.957826086957, 15776.042173913043, 41817.0, 'Саратов'], [7, '11.02.21', '128', 'ИП Михеева Нина Владимировна', 164513.3, 98290.42557625014, 66222.87442374985, 0.0, 'Саратов'], [8, '15.02.21', '136', 'ИП Сапогова Таисия Владимировна', 2549.52, 1578.6182582582583, 970.9017417417417, 0.0, 'Саратов'], [9, '17.02.21', '147', 'ИП Сапогова Таисия Владимировна', 3961.67, 2319.8846795541626, 1641.7853204458374, 0.0, 'Саратов'], [10, '17.02.21', '148', 'ООО "ЕВРОПЛАСТ-Ф"', 110840.93, 66748.75563489055, 44092.174365109444, 0.0, 'Саратов'], [11, '18.02.21', '150', 'ИП Ибрагимов Станислав Станиславович', 14706.52, 8014.420342184811, 6692.09965781519, 14706.52, 'Саратов'], [12, '19.02.21', '156', 'ИП Сапогова Таисия Владимировна', 11137.56, 7491.988688688689, 3645.5713113113106, 0.0, 'Саратов'], [13, '25.02.21', '161', 'ИП Сапогова Таисия Владимировна', 11921.56, 6314.473033033033, 5607.086966966966, 0.0, 'Саратов'], [14, '25.02.21', '162', 'ИП Ибрагимов Станислав Станиславович', 13920.49, 5610.621196914541, 8309.86880308546, 13920.49, 'Саратов'], [15, '25.02.21', '163', 'ИП Исаев Дмитрий Викторович', 16218.0, 8513.671304347827, 7704.328695652173, 0.0, 'Саратов'], [16, '28.02.21', '179', 'Ульяновск ч\\л', 307849.8, 249809.60947288322, 58040.19052711676, 0.0, 'Саратов'], ['', '', '', '', 854015.06, 563073.3998033099, 604205.4505271169, 159422.19999999998, ''], [[1, '06.01.2021', '1', 'ООО "ЭРА"', 78000.0, '', '', 78000.0], [2, '28.01.2021', '85', 'ИП Сапогова Таисия Владимировна', 271949.0, '', '', 271949.0], [3, '22.01.2021', '56', 'ИП Сапогова Таисия Владимировна', 2097827.0, '', '', 2097827.0], [4, '02.02.2021', '90', 'ИП Сапогова Таисия Владимировна', 1908000.0, '', '', 1908000.0], [5, '18.01.2021', '39', 'ИП Сапогова Таисия Владимировна', 1372582.0, '', '', 1372582.0], [6, '21.01.2021', '54', 'ИП Сапогова Таисия Владимировна', 487257.0, '', '', 487257.0], [7, '05.02.2021', '107', 'ИП Потужная Марина Викторовна', 6942309.0, '', '', 6942309.0], [8, '05.02.2021', '104', 'ООО "ТАРСК-НСК"', 250000.0, '', '', 250000.0], [9, '30.12.2020', '752', 'ООО "БМ ГРУПП"', 17698579.0, '', '', 17698579], [10, '09.12.2020', '681', 'ООО "БМ ГРУПП"', 855000.0, '', '', 855000.0], [11, '17.12.2020', '231', 'ООО "ЭРА"', 9464000.0, '', '', 9464000.0], [12, '11.01.2021', '6', 'ООО "ТЕКСФОМ"', 588000.0, '', '', 588000.0], [13, '14.01.2021', '25', 'ООО "ТЕКСФОМ"', 588000.0, '', '', 588000.0], [14, '15.01.2021', '34', 'ООО "ТЕКСФОМ"', 1176000.0, '', '', 1176000.0], [15, '18.01.2021', '37', 'ООО "ТЕКСФОМ"', 8496398.0, '', '', 8496398.0], [16, '17.12.2020', '710', 'ООО "ТАТСТРОЙКАМА"', 672733.0, '', '', 672733.0], [17, '22.01.2021', '60', 'ООО "ЭРА"', 1137500.0, '', '', 1137500.0], [18, '20.01.2021', '48', 'ООО "ЭРА"', 4607280.0, '', '', 4607280.0], [19, '22.12.2020', '719', 'ООО "ЕВРОПЛАСТ-Ф"', 7129392.0, '', '', 7129392.0], [20, '22.01.2021', '59', 'ООО "ЭРА"', 8260056.0, '', '', 8260056.0], [21, '03.02.2021', '101', 'ООО "МТ-СИБИРЬ"', 2760000.0, '', '', 2760000.0], [22, '27.01.2021', '72', 'ООО "ЕВРОТЕКС СТИЛЬ"', 57182518.0, '', '', 57182518], [23, '27.01.2021', '70', 'ООО "ЕВРОТЕКС СТИЛЬ"', 14700900.0, '', '', 14700900], [24, '27.01.2021', '71', 'ООО "ЕВРОТЕКС СТИЛЬ"', 12062142.0, '', '', 12062142]]]

def xlsx_writer_train():
    workbook = xlsxwriter.Workbook('pfo_report.xlsx')
    worksheet = workbook.add_worksheet('temporary1')
    col= 0
    for row, data in enumerate(data_linked):
        worksheet.write_row(row, col, data)
    workbook.close()

dd={}
d = {1: [1, 2]}
d[5] = d.get(5, 0) + 5
d[5] = d.get(5, 0) + 5
dd.update(d)
print(dd)

