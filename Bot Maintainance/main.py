import telebot
import datetime 
from datetime import datetime
import os
import keep_alive
from replit import db

BOT_TOKEN = os.environ['BOT_KEY']
bot = telebot.TeleBot(BOT_TOKEN)
CHAT = os.environ['CHAT']

@bot.message_handler()
def maintainance(message):
  bot.send_message(message.chat.id, "Bot Is Under Maintainance Now")
bot.infinity_polling()
keep_alive.keep_alive()
