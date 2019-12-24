import datetime
import os
import telebot
import urllib
import yaml

import search_engine

from io import BytesIO
from cinema_bot_exception import CinemaBotException


WELCOME_MESSAGE = r"""
Hello, i'm cinemabot by Vladimir Kuznetsov (v.j.kuznetsov@gmail.com)
Allowed coomands:
/find - looking for a link to watching a movie
/info - print summary about the movie
/poster - print poster
"""

API_KEY_EXCEEDED_MESSAGE = r"""
Error: api_key exceeded, please contact the administrator"""

ERROR_MESSAGE = r"""
An error occurred during the search, please contact the administrator."""

# load configuration
with open('cfg.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)

# load tokens
telegram_token = os.getenv('TELEGRAM_TOKEN')
cfg_se = cfg['search_engine']
cfg_se['api_key'] = os.getenv('SE_TOKEN')


def _check_api_key_expired(cfg):
    """Return true if search engine api key expired

    Arguments:
    cfg -- dict with configuration from yaml
    """
    expired_day = cfg["serpapi"]["expired_date"]
    expired_day_dt = datetime.datetime.strptime(expired_day, '%Y-%m-%d')
    return expired_day_dt < datetime.datetime.now()


def _exc_logger(message, exc):
    """Logged error

    Arguments:
    message -- received messages
    exc -- exception object"""
    print(f"{datetime.datetime.now()}: Exception raises:\
          {exc.args} after income message: {message}")


bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if _check_api_key_expired:
        bot.reply_to(message, API_KEY_EXCEEDED_MESSAGE)
    else:
        bot.reply_to(message, WELCOME_MESSAGE)


@bot.message_handler(commands=['find'])
def search_watch(message):
    message_text = message.text.lstrip('/find')
    try:
        result = search_engine.watch(message_text, cfg_se)
        bot.send_message(message.chat.id, result)
    except CinemaBotException as exc:
        _exc_logger(message, exc)
        bot.send_message(message.chat.id, ERROR_MESSAGE)


@bot.message_handler(commands=['info'])
def search_info_(message):
    message_text = message.text.lstrip('/info')
    try:
        wiki_summary = search_engine.info(message_text, cfg_se)
        bot.send_message(message.chat.id, wiki_summary)
    except CinemaBotException as exc:
        _exc_logger(message, exc)
        bot.send_message(message.chat.id, ERROR_MESSAGE)


@bot.message_handler(commands=['poster'])
def search_poster_(message):
    message_text = message.text.lstrip('/poster')
    try:
        result_link = search_engine.poster(message_text, cfg_se)
        bot.send_photo(message.chat.id,
                       BytesIO(urllib.request.urlopen(result_link).read()))
    except CinemaBotException as exc:
        _exc_logger(message, exc)
        bot.send_message(message.chat.id, ERROR_MESSAGE)


if __name__ == '__main__':
    bot.polling()
