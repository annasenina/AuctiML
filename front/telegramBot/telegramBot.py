import telebot
from env import botToken

bot = telebot.TeleBot(botToken)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Введите номер лота на сайте torgi.gov.ru: ")
    else:
        bot.send_message(message.from_user.id, "Спасибо, вы ввели номер лота: "+message.text)

bot.polling(none_stop = True, interval = 0)