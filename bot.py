import yaml
import telebot
import urllib
import os
from io import BytesIO
from search_engine import search_watch, search_poster, search_info


with open("cfg.yml","r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)

telegram_token = os.environ['TELEGRAM_TOKEN']
search_engine_token = os.environ['SE_TOKEN']
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm simple echo bot. Tell me something!")

@bot.message_handler(func=lambda m: True)
def search_watch_(message):
    result_link = search_watch(message=message, cfg=cfg)
    bot.reply_to(message, result_link)

@bot.message_handler(commands=['info'])
def search_info_(message):
    wiki_summary = search_info(message, cfg)
    bot.reply_to(message, wiki_summary)


@bot.message_handler(commands=['poster'])
def search_poster_(message):
    result_link = search_poster(message, cfg)
#    f = open('tmp.jpg', 'wb')
#    f.write(urllib.request.urlopen(result_link).read())
#    bot.send_photo(message.chat.id, f)
    bot.send_photo(message.chat.id, img=BytesIO(urllib.request.urlopen(result_link).read()))


if __name__ == '__main__':
    bot.polling()
