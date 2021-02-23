""" telebot that sends files and statistic information """
# -*- coding: utf8 -*-
import telebot
import configparser
import sales_control
import finance
import Alex_debt
import Scraping

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
keyboard1.row('Просрочка(файл)', 'Остатки на счетах', 'Рентаб. < 30%', 'Цены')


@bot.message_handler(commands=['start'])  # decorator
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я сервисный бот', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if str(message.chat.id) in company_ids:
        employee_name = conf['TeleBot'][str(message.chat.id)]
        # debt file
        if message.text.lower() == 'просрочка(файл)':
            bot.send_message(message.chat.id, f'Файл дебетовой задолженности формируется, подождите!')
            alex_file_data = Alex_debt.get_otgruzka_list()
            debt_f = open(alex_file_data[0], 'rb')
            bot.send_document(message.chat.id, debt_f)
            bot.send_message(message.chat.id,
                             f'Общая задолженность {alex_file_data[2]} по отгрузкам {alex_file_data[1]}руб.')
        # account remains
        elif message.text.lower() in ['остатки на счетах', 'остатки']:
            account_sum = finance.get_account_summ()
            bot.send_message(message.chat.id, f'Остаток денег на рублевых счетах {account_sum}руб.')
        # low profits
        elif message.text.lower() in ['рентаб. < 30%', 'рентаб']:
            sales_list = sales_control.get_sales_list()
            if len(sales_list) > 0:
                for sale in sales_control.get_sales_list():
                    bot.send_message(message.chat.id,
                                     f'Клиент {sale[0]} на сумму {sale[1]}руб. рентабельность(вал) {sale[2]}%')
            else:
                bot.send_message(message.chat.id, f'Отгрузок с рентабельностью ниже 30% не обнаружено.')
        # forest price
        #elif message.text.lower() in ['прайс', 'форест']:
        #    scrapped = Scraping.run_scrapy()
        #    my_book_link = 'https://docs.google.com/spreadsheets/d/1_C6uxRFz5wb8K_Cu4c4HcUn8EYk0vnhARhA_UvtKT1c/edit#gid=0'
        #    bot.send_message(message.chat.id, f'Сравнение цен по ссылке {my_book_link}')
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


bot.polling()
