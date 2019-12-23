import yaml
import telebot
import urllib
import os
from io import BytesIO
from search_engine import search_watch, search_poster, search_info


with open("cfg.yml","r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)

telegram_token = os.getenv('TELEGRAM_TOKEN')
cfg['api_key'] = os.getenv('SE_TOKEN')

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm simple echo bot. Tell me something!")

@bot.message_handler(commands=['find'])
def search_watch_(message):
    message_text = message.text.lstrip('/find')
    result_link = search_watch(message=message_text, cfg=cfg)
    bot.reply_to(message, result_link)

@bot.message_handler(commands=['info'])
def search_info_(message):
    message_text = message.text.lstrip('/info')
    wiki_summary = search_info(message_text, cfg)
    bot.reply_to(message, wiki_summary)


@bot.message_handler(commands=['poster'])
def search_poster_(message):
    message_text = message.text.lstrip('/poster')
    result_link = search_poster(message_text, cfg)
    bot.send_photo(message.chat.id, BytesIO(urllib.request.urlopen(result_link).read()))

if __name__ == '__main__':
    bot.polling()
