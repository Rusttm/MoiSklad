# -*- coding: utf8 -*-
import xlsxwriter
from datetime import date

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

            customer_name =''
            cell_row_group = 2
            shift_row=1
            # insert data
            for row_num, row_data in enumerate(data_linked):

                for col_num, col_data in enumerate(row_data):
                    if col_num == 3 : new_customer_name = col_data
                if customer_name != new_customer_name:
                    cell_row_group = 2
                    alex_worksheet.set_row(row_num + shift_row, None, None, {'level': cell_row_group})
                    alex_worksheet.write(row_num + shift_row, col_num, col_data)
                else:
                    cell_row_group = 1
                    alex_worksheet.write(row_num+shift_row, 3, customer_name)
                    alex_worksheet.set_row(row_num + shift_row, None, None, {'level': cell_row_group})
                    shift_row += 1




            alex_workbook.close()
        except Exception:
            print('Error, cant create file', Exception)

    except Exception:
        print('Error cant fill the DataFrame', Exception)


fill_the_df(data_linked)
