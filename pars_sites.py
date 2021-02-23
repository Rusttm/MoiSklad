""" module write parsed information to google books"""


from datetime import datetime
import xlsxwriter
from datetime import date
import configparser





def fill_the_df(data_linked):
    try:
        columns_for_df = ['Дата формирования отчета', 'Группы покупателя', 'Покупатель',
                          'Номер и дата отгрузки', 'Отсрочка, дней', 'Дней до оплаты',
                          'Размер просроченной задолженности', 'Статус', 'ссылка на документ']
        '''write to excell'''
        data_linked = sorted(data_linked, key=lambda y: (y[1], y[2], y[3]))  # sorting by group and name
        try:
            today = date.today()
            file_date = str(today.strftime("%d.%m.%y"))
            file_name = str('alex_debt_%s.xlsx' % today)
            alex_workbook = xlsxwriter.Workbook(file_name)
            alex_worksheet = alex_workbook.add_worksheet(str(today.strftime("%d-%m-%y")))
            bold = alex_workbook.add_format({'bold': True})

            # insert top line
            for col_num, col_data in enumerate(columns_for_df):
                alex_worksheet.write(0, col_num, col_data, bold)

            customer_name = 'Покупатель'
            start_row = 1
            shift_row = 1  # shifting for write total sum
            doc_sum = 0
            row_num = 0
            # write data to file and insert Total sums
            for row_num, row_data in enumerate(data_linked):
                new_customer_name = row_data[2]
                doc_sum += float(row_data[6])
                if not ((customer_name == new_customer_name) or (customer_name == 'Покупатель')):
                    alex_worksheet.set_row(row_num + shift_row, None, None, {'level': 0})
                    alex_worksheet.write(row_num + shift_row, 0, customer_name, bold)
                    alex_worksheet.write(row_num + shift_row, 5, 'Всего', bold)
                    alex_worksheet.write(row_num + shift_row, 6, f'=SUM(G{start_row}:G{row_num+ shift_row})', bold)
                    shift_row += 1
                    start_row = row_num + shift_row + 1
                alex_worksheet.set_row(row_num + shift_row, None, None, {'level': 1})
                for col_num, col_data in enumerate(row_data):
                    alex_worksheet.write(row_num + shift_row, col_num, col_data)
                customer_name = new_customer_name
            '''make last customer summary'''
            alex_worksheet.write(row_num + shift_row+1, 0, customer_name, bold)
            alex_worksheet.write(row_num + shift_row+1, 5, 'Всего', bold)
            alex_worksheet.write(row_num + shift_row+1, 6, f'=SUM(G{start_row}:G{row_num + shift_row+1})', bold)

            '''make all customer summary'''
            alex_worksheet.write(row_num + shift_row+2, 0, 'По всем клиентам', bold)
            alex_worksheet.write(row_num + shift_row+2, 2, doc_sum, bold)
            alex_workbook.close()
            return [file_name, round(doc_sum, 2), file_date]
        except IndexError:
            print('Error, cant create file', Exception)
            return [False, False, False]
    except IndexError:
        print('Error cant fill the DataFrame', Exception)
        return [False, False, False]