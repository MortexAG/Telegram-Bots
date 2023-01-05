import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import keep_alive
import threading
import time

mongo_connect = os.environ['mongo_connect']
BOT_API = os.environ['BOT_API']
owner_1 = str(os.environ['owner_1'])
owner_2 = str(os.environ['owner_2'])

owners_list = [owner_1, owner_2]
cluster = MongoClient(mongo_connect)
db = cluster["anakin_care"]
food = db['food_time']

bot = telebot.TeleBot(BOT_API)

def main_bot():

  def get_hours():
    time_now = datetime.now()
    hours = int(time_now.strftime("%H"))
    accurate = hours+2
    return accurate

  def get_minutes():
    time_now = datetime.now()
    minutes = int(time_now.strftime("%M"))
    return minutes

  def get_time():
    hours = get_hours()
    minutes = get_minutes()
    #time_now = datetime.now()
    #hours = time_now.strftime("%H")
    #accurate = int(hours)+2
    times = str(hours)+":"+str(minutes)
    return times

  def keyboard(key_type="Normal"):
      markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
      if key_type == "Normal":
          markup.add(KeyboardButton('Add Food'))
          markup.add(KeyboardButton('Last Food Time'))
          markup.add(KeyboardButton('Next Food Time'))

      return markup

  @bot.message_handler(commands=["start", "keyboard"])
  def start_message(message):
    if str(message.from_user.id) in owners_list:
      bot.send_message(message.chat.id,"You can use the keyboard",reply_markup=keyboard())
    else:
      bot.send_message(message.from_user.id, "You Don't Have Permission To Use The Bot")
  @bot.message_handler(commands=["link", "site"])
  def site(message):
    if str(message.from_user.id) in owners_list:
      bot.send_message(message.chat.id,"Here's A Link To Follow Up: https://anakin-care.mortexag.repl.co")
    else:
      bot.send_message(message.from_user.id, "You Don't Have Permission To Use The Bot")
  @bot.message_handler(commands=["source", "owner", "creator"])
  def source(message):
    if str(message.from_user.id) in owners_list:
      bot.send_message(message.chat.id,"This Bot Was Made By @MortexAG Using Python")
      bot.send_message(message.chat.id, "Here's My Source Code: https://github.com/MortexAG/Telegram-Bots/tree/main/Anakin%20Care%20Bot")
    else:
      bot.send_message(message.from_user.id, "You Don't Have Permission To Use The Bot")


  @bot.message_handler(func=lambda message:True)
  def all_messages(message):
    if str(message.from_user.id) in owners_list:
      if message.text == "Add Food":
        times = get_time()
        hours = get_hours()
        minutes = get_minutes()
        next_h= int(hours) + 12
        if int(next_h) >= 24:
          next_h = abs(int(next_h) - 24)
        next_time = str(next_h)+":"+str(minutes)
        #list = food.find_one({"_id":0})
        filter = {"_id":0}
        newvalues = {"$set":{"feeder":message.from_user.username, "last_time":times, "next_time_number":int(next_h), "next_time":next_time}}
        food.update_one(filter, newvalues)
        bot.send_message(message.from_user.id, f"{message.from_user.username} Added Food At {times} Next Food Time in 12 Hours")
      elif message.text == "Last Food Time":
        stats = food.find_one({"_id":0})
        last_time = stats['last_time']
        last_feeder = stats['feeder']
        next_hours = stats['next_time_number']
        next_time = stats['next_time']
        now_h = get_hours()
        remain_h = abs(int(next_hours) - int(now_h))
        bot.send_message(message.from_user.id,f"Last Feeding Time Was {last_time} And Was Done By {last_feeder}")
        bot.send_message(message.from_user.id, f"Next time will Be at {next_time}, which is {remain_h} hours from now")
      elif message.text == "Next Food Time":
        stats = food.find_one({"_id":0})
        next_hours = stats['next_time_number']
        next_time = stats['next_time']
        now_h = get_hours()
        remain_h = abs(int(next_hours) - int(now_h))
        bot.send_message(message.from_user.id, f"Next time will Be at {next_time}, which is {remain_h} hours from now")
      else:
        bot.send_message(message.from_user.id, "Don't Send Messages To The Bot, Use The Keyboard Please")
    else:
      bot.send_message(message.from_user.id, "You Don't Have Permission To Use The Bot")
def reminder():
    def get_hours():
      time_now = datetime.now()
      hours = int(time_now.strftime("%H"))
      accurate = hours+2
      return accurate
    while (True):
      feeding = food.find_one({"_id":0})
      next_time = feeding['next_time_number']
      now = get_hours()
      if int(now) == (next_time):
        for i in owners_list:
          bot.send_message(i, f"it's {next_time}, please add food to Anakin")
      time.sleep(600)



background_loop = threading.Thread(name='reminder',daemon = True, target=reminder)
the_main = threading.Thread(name='main', target=main_bot)

background_loop.start()
the_main.start()
    
bot.infinity_polling()
keep_alive.keep_alive()
