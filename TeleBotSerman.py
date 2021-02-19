''' telebot that sends files and statistic information '''
# -*- coding: utf8 -*-
import telebot
import configparser
import sales_control

#curl -v -F "chat_id=569502265" -F document=@/Users/users/Desktop/file.txt https://api.telegram.org/bot<TOKEN>/sendDocument

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


account_sum = str(float(conf['MoiSklad']['account_sum'])/100)
account_date = conf['MoiSklad']['account_date']
#prepare xlsx file
debt_file = str(conf['MoiSklad']['last_debt_file'])
debt_file_sum = int(conf['MoiSklad']['debt_file_sum'])
debt_f = open(debt_file,'rb')
#run the bot
bot = telebot.TeleBot(bot_token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True) #1st True - shrink keyborad 2nd  True  -hide keyboard
keyboard1.row('Просрочка(файл)', 'Остатки на счетах', 'Рентаб. < 30%')

@bot.message_handler(commands=['start'])  #decorator
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я сервисный бот', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if str(message.chat.id) in company_ids:
        employee_name = conf['TeleBot'][str(message.chat.id)]
        bot.send_message(message.chat.id, f'Здравствуйте, {employee_name}')
        # debt file
        if message.text.lower() == 'просрочка(файл)':
            bot.send_message(message.chat.id, f'Файл дебетовой задолженности формируется!')
            bot.send_document(message.chat.id, debt_f)
            bot.send_message(message.chat.id, f'Общая задолженность по отгрузкам {debt_file_sum}руб.')
        # account remains
        elif message.text.lower() in ['остатки на счетах', 'остатки']:
            bot.send_message(message.chat.id, f'На {account_date} остаток денег на счетах {account_sum}руб.')
        # low profits
        elif message.text.lower() in ['рентаб. < 30%', 'рентаб']:
            for sale in sales_control.get_sales_list():
                bot.send_message(message.chat.id, f'Клиент {sale[0]} на сумму {sale[1]}руб. рентабельность(вал) {sale[2]}%')
        # unknown command
        else:
            bot.send_message(message.chat.id, f'{employee_name}, команда {message.text} не опознана!')
    # unknown employee
    else: bot.send_message(message.chat.id, f'Пользователь с id {message.chat.id} не зарегистрирован. Пожалуйста, пройдите регистрацию')


@bot.message_handler(content_types=['sticker'])
def send_sticker_id(message):
    bot.send_message(message.chat.id, f'your sticker id is {sticker_id}')
    bot.send_sticker(message.chat.id, sticker_id)

bot.polling()



