""" telebot that sends files and statistic information """
# -*- coding: utf8 -*-
import telebot
import configparser
import sales_control
import finance
import Alex_debt
import reports
import customers_debt
import time
import schedule
from threading import Thread
from datetime import datetime


conf = configparser.ConfigParser()
conf.read('bot.ini')

my_chat_id = conf['TeleBot']['my_chat_id']
bot_token = conf['TeleBot']['bot_token']
bot_user_name = conf['TeleBot']['bot_user_name']
sticker_id = conf['TeleBot']['sticker_id']
command = conf['TeleBot']['macos_command']
company_ids = [str(conf['TeleBot']['my_chat_id']),
               str(conf['TeleBot']['minasyan_id']),
               str(conf['TeleBot']['alex_id']),
               str(conf['TeleBot']['mans_id'])]

bot = telebot.TeleBot(bot_token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)  # 1st True - shrink keyboard 2nd  True  -hide keyboard
keyboard1.row('Просрочка(ссылка)', 'Остатки на счетах', 'Рентаб. < 30%', 'Цены', 'Отчет', 'Задолженность')


@bot.message_handler(commands=['start'])  # decorator
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я сервисный бот', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    event = f'{time.ctime(message.date)}; {message.chat.id}; {message.chat.first_name}; {message.text} \n'
    print(event)
    with open("bot_log.txt", "a") as myfile:
        myfile.write(event)
    if str(message.chat.id) in company_ids:
        employee_name = conf['TeleBot'][str(message.chat.id)]
        # debt file
        if message.text.lower() == 'просрочка(ссылка)':
            #bot.send_message(message.chat.id, f'Файл дебетовой задолженности формируется, подождите!')
            #alex_file_data = Alex_debt.get_otgruzka_list()
            #файл не высылается c 02-06-21
            #debt_f = open(alex_file_data[0], 'rb')
            #bot.send_document(message.chat.id, debt_f)
            #debt_link = 'https://docs.google.com/spreadsheets/d/1NUJo6PmTgfZ8OvXnl8tSPEv6DNwWXA4WXBquBAznJ3g/edit#gid=0'
            #markdown = f'На {alex_file_data[2]} просрочено <a href="{debt_link}">{alex_file_data[1]}руб.</a>'
            #bot.send_message(message.chat.id, markdown, parse_mode='html')
            alex_debt_link = 'https://docs.google.com/spreadsheets/d/1ZSfXugnudJHYnGHxLQaU1W7iIQwFrIiFGsGkpR7jbwE/edit#gid=0'
            markdown2 = f'<a href="{alex_debt_link}">Расчеты просроченной задолженности</a>'
            bot.send_message(message.chat.id, markdown2, parse_mode='html')
        # debt
        elif message.text.lower() in ['задолженность', 'долги']:
            bot.send_message(message.chat.id, f'Запрашиваю данные, подождите!')
            c_debt = customers_debt.get_customers_balance()
            for group in c_debt['Покупатели']:
                bot.send_message(message.chat.id, f'{group} : {int(c_debt["Покупатели"][group])}руб.')
        # account remains
        elif message.text.lower() in ['остатки на счетах', 'остатки']:
            account_sum = finance.get_account_summ()
            markdown = f"<b>Остаток денег</b> на рублевых счетах {int(account_sum)}руб."
            bot.send_message(message.chat.id, markdown, parse_mode='html')
        # actual profit
        elif message.text.lower() in ['прибыль', 'отчет', 'отчет по прибыли', 'оборот']:
            bot.send_message(message.chat.id, f'Файл отчетности формируется, подождите!')
            profit_sum = reports.actual_report()
            href_link = profit_sum[1]
            markdown = f'Текущая прибыль по месяцу <a href="{href_link}">{profit_sum[0]}руб.</a>'
            bot.send_message(message.chat.id, markdown, parse_mode='html')
            #bot.send_message(message.chat.id, f'Расчет прибыли по ссылке {profit_sum[1]}')
        # low profits
        elif message.text.lower() in ['рентаб. < 30%', 'рентаб']:
            sales_list = sales_control.get_sales_list()
            if len(sales_list) > 0:
                for sale in sales_control.get_sales_list():
                    markdown = f'Клиент <b>{sale[0]}</b> на сумму {sale[1]}руб. рентабельность(вал) {int(sale[2])}%'
                    bot.send_message(message.chat.id, markdown, parse_mode='html')
            else:
                bot.send_message(message.chat.id, f'Отгрузок с рентабельностью ниже 30% не обнаружено.')
        # forest price
        elif message.text.lower() in ['прайс', 'цены', 'форест']:
        #    scrapped = Scraping.run_scrapy()
            my_book_link = 'https://docs.google.com/spreadsheets/d/1_C6uxRFz5wb8K_Cu4c4HcUn8EYk0vnhARhA_UvtKT1c/edit#gid=0'
            #markdown = "<a href='"+my_book_link+"'>Сравнение цен</a>"
            markdown = f'<a href="{my_book_link}">Сравнение цен</a>'
            bot.send_message(message.chat.id, markdown, parse_mode='html')
        # unknown command
        else:
            bot.send_message(message.chat.id, f'{employee_name}, команда {message.text} не опознана!')
    # unknown employee
    else:
        bot.send_message(message.chat.id,
                         f'Пользователь с id {message.chat.id} не зарегистрирован. Пожалуйста, пройдите регистрацию')


@bot.message_handler(content_types=['sticker'])
def send_sticker_id(message):
    bot.send_message(message.chat.id, f'your sticker id is {sticker_id}')
    bot.send_sticker(message.chat.id, sticker_id)

def send_report():
    chat_id = company_ids[3]
    #рассылка только в рабочие дни
    if datetime.now().weekday() not in [5, 6]:
        form_date = str(datetime.now().strftime("%d:%m:%y"))
        message_component = ''
        #отчет по задолженности покупателей
        c_debt = customers_debt.get_customers_balance()
        all_cusomers_debt = c_debt['Покупатели']['Итого']
        message_component += f'Отчеты на {form_date}:\n'
        message_component += f'<b>Задолженность</b> по клиентам {all_cusomers_debt}руб.\n'
        #отчет по продажам меньше 30
        sales_list = sales_control.get_sales_list()
        if len(sales_list) > 0:
            message_component += f'Низкая <b>рентабельность</b>:\n'
            for sale in sales_control.get_sales_list():
                message_component += f'{sale[0]} {sale[1]}руб. {int(sale[2])}%;\n'
        else:
            message_component += f'Отгрузок с рентабельностью ниже 30% не обнаружено.\n'
        #прибыль по месяцу
        profit_sum = reports.actual_report()
        message_component += f'Текущая <b>прибыль</b> по месяцу {profit_sum[0]}руб.\n'
        bot.send_message(chat_id, message_component, parse_mode='html')
    else:
        bot.send_message(chat_id, 'Хороших Вам выходных!')
def daily_report():
    schedule.every().day.at("17:00").do(send_report)
    while True:
        schedule.run_pending()
        time.sleep(1)  # Выберите оптимальное значение под свои задачи планировщика

# Создаём и запускаем планировщик в отдельном потоке
t = Thread(target=daily_report)
t.start()


if __name__ == '__main__':
    bot.infinity_polling()
