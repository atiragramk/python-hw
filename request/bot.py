import os
import telebot
from giphy import search_gifs

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def welcome_reply(message):
    bot.reply_to(message, "How are you doing, bro?")


@bot.message_handler(commands=['search'])
def search_handler(message):
    text = "What gifs are you looking for?"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, count_handler)


def count_handler(message):
    query = message.text
    text = "Type a number of needed gifs"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_gifs, query)


def fetch_gifs(message, query):
    try:
        limit = message.text
        url_list = search_gifs(query, limit)
        for url in url_list:
            bot.send_animation(message.chat.id, url)
    except Exception:
        url = 'https://media2.giphy.com/media/M9yC8b0x7Y7oA/giphy.gif?cid=ecf05e47uj5vjnvl8414jemml335k4p6rwvpx4v1gpckogca&ep=v1_gifs_search&rid=giphy.gif&ct=g'
        bot.send_animation(
            message.chat.id, url, caption='Something went wrong')


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


def run_bot():
    bot.infinity_polling()
