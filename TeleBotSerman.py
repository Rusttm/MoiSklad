''' telebot that sends files and statistic information '''

import telebot
import configparser

#curl -v -F "chat_id=569502265" -F document=@/Users/users/Desktop/file.txt https://api.telegram.org/bot<TOKEN>/sendDocument

conf = configparser.ConfigParser()
conf.read('bot.ini')

my_chat_id = conf['TeleBot']['my_chat_id']
bot_token = conf['TeleBot']['bot_token']
bot_user_name = conf['TeleBot']['bot_user_name']
sticker_id = conf['TeleBot']['sticker_id']
command = conf['TeleBot']['macos_command']
company_ids = [str(conf['TeleBot']['my_chat_id']),  str(conf['TeleBot']['alex_id'])]

debt_file=str(conf['MoiSklad']['last_debt_file'])
debt_f = open(debt_file,'rb')

bot = telebot.TeleBot(bot_token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True) #1st True - shrink keyborad 2nd  True  -hide keyboard
keyboard1.row('Просрочка(файл)', 'Отчет за день')

@bot.message_handler(commands=['start'])  #decorator
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я сервисный бот', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if str(message.chat.id) in company_ids:
        emploee_name = conf['TeleBot'][str(message.chat.id)]
        bot.send_message(message.chat.id, f'Здравствуйте {emploee_name}')
        if message.text.lower() == 'просрочка(файл)':
                bot.send_document(message.chat.id, debt_f)
        else: bot.send_message(message.chat.id, f'{emploee_name}, комманда не опознана!')

    else: bot.send_message(message.chat.id, f'Пользователь с id {message.chat.id} не зарегистрирован. Пожалуйста, пройдите регистрацию')


def load_file_to_ttelegram():
    return True

@bot.message_handler(content_types=['sticker'])
def send_sticker_id(message):
    bot.send_message(message.chat.id, f'your sticker id is {sticker_id}')
    bot.send_sticker(message.chat.id, sticker_id)

bot.polling()



