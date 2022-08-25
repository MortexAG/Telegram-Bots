import telebot
import os
import keep_alive


BOT_TOKEN = os.environ['BOT_KEY']
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler()
def maintainance(message):
  bot.send_message(message.chat.id, "Bot Is Under Maintainance Now")
bot.infinity_polling()
keep_alive.keep_alive()
