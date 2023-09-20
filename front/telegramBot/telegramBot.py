import telebot
from env import botToken
import requests

bot = telebot.TeleBot(botToken)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Введите url лота на сайте torgi.gov.ru: ")
    else:
        responce = requests.post('http://127.0.0.1:8000/predict', json={"url": message.text})
        bot.send_message(message.from_user.id, "Спасибо, вы url лота: "+responce.text)

bot.polling(none_stop = True, interval = 0)