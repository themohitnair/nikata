import telebot
import os
from dotenv import load_dotenv

load_dotenv()

help_message = r"""

\- For project info, visit our [Github README](https://github\.com/themohitnair/nikata)\.

\- To receive chatID of the notified from this bot, send '/start' to the bot\.

\- If you are an app user, you can use the Telegram IDs of those you want to inform, to initiate conversation with this bot \- [@nikatadoota\_bot](https://t\.me/nikatadoota\_bot)\.
"""


TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="MarkdownV2")

@bot.message_handler(commands=['start'])
def welcome_chatID(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"ChatID: `{chat_id}`", parse_mode="MarkdownV2")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, help_message, parse_mode="MarkdownV2")

bot.infinity_polling()
