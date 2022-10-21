import telebot
import datetime 
from datetime import datetime
import os
import keep_alive

BOT_TOKEN = os.environ['BOT_KEY']
bot = telebot.TeleBot(BOT_TOKEN)
CHAT = os.environ['CHAT']

@bot.message_handler(commands=['start'])
def daily_msg(message):
  bot.send_message(message.chat.id, "Welcome To The Good Morning Text Bot, Use /subscribe To Start Getting Daily Messages, If You Want to Deactivate The Daily Messages Stop The Bot")
@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, "Use /subscribe To Start Getting Daily Messages, If You Want to Deactivate The Daily Messages Stop The Bot")


  
@bot.message_handler(commands=['subscribe'])

def subscribe(message):
  bot.send_message(message.chat.id, "You Will Start Recieving Daily Good Morning Texts at 6AM GMT.")
  while (True):
    import time
    now = datetime.now()
    today = datetime.today()
    weekday = today.strftime('%A')
    day = today.strftime("%d/%m")
    current_time = now.strftime("%H")
    if current_time == "06":
      bot.send_message(message.chat.id, "Good Morning, It's {}, {}, Have a Nice Day".format(weekday, day))
      time.sleep(3600)

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
  bot.send_message(message.chat.id, "You're Now Unsubscribed From The Daily Good Morning Text.")
  
      
bot.infinity_polling()
keep_alive.keep_alive()
