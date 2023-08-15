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
import random

# Configure The Bot Info
cat_name = "Anakin"
time_interval = int(12)
time_zone = int(3)
site_link = "https://anakin-care.mortexag.repl.co"
mongo_connect = os.environ['mongo_connect']
BOT_API = os.environ['BOT_API']
owner_1 = str(os.environ['owner_1'])
owner_2 = str(os.environ['owner_2'])
owners_list = [owner_1, owner_2]
cluster = MongoClient(mongo_connect)
db = cluster["anakin_care"]
food = db['food_time']
points = db['points']

bot = telebot.TeleBot(BOT_API)

# confiormation variable 
confirm = False

def main_bot():

  def get_hours():
    time_now = datetime.now()
    hours = int(time_now.strftime("%H"))
    accurate = hours + int(time_zone)
    return accurate

  def get_minutes():
    time_now = datetime.now()
    minutes = int(time_now.strftime("%M"))
    if minutes < 10:
      minutes = str(0) + str(minutes)
      return minutes
    return int(minutes)

  def get_time():
    hours = get_hours()
    minutes = get_minutes()
    #time_now = datetime.now()
    #hours = time_now.strftime("%H")
    #accurate = int(hours)+2
    times = str(hours) + ":" + str(minutes)
    return times

  def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if key_type == "Normal":
      markup.add(KeyboardButton('Add Food'))
      markup.add(KeyboardButton('Score'))
      markup.add(KeyboardButton('Last Food Time'))
      markup.add(KeyboardButton('Next Food Time'))
    elif key_type == "Confirm":
      markup.add(KeyboardButton('Yes'))
      markup.add(KeyboardButton('No'))
    return markup



# giving the keyboard after checking permission

  @bot.message_handler(commands=["start", "keyboard"])
  def start_message(message):
    # check if the user is allowed to use the bot
    if str(message.from_user.id) in owners_list:
      bot.send_message(message.chat.id,
                       "You can use the keyboard",
                       reply_markup=keyboard())
    else:
      bot.send_message(message.from_user.id,
                       "You Don't Have Permission To Use The Bot")

    # get the bot's site which has the feeder name and the times

  @bot.message_handler(commands=["link", "site"])
  def site(message):
    # check if the user is allowed to use the bot
    if str(message.from_user.id) in owners_list:
      bot.send_message(message.chat.id,
                       f"Here's A Link To Follow Up: {site_link}")
    else:
      bot.send_message(message.from_user.id,
                       "You Don't Have Permission To Use The Bot")

    # get the bot's source code

  @bot.message_handler(commands=["source", "owner", "creator"])
  def source(message):
    # check if the user is allowed to use the bot
    if str(message.from_user.id) in owners_list:
      bot.send_message(message.chat.id,
                       "This Bot Was Made By @AhmedGouda100 Using Python")
      bot.send_message(
        message.chat.id,
        "Here's My Source Code: https://github.com/MortexAG/Telegram-Bots/tree/main/Cat%20Care%20Bot"
      )
    else:
      bot.send_message(message.from_user.id,
                       "You Don't Have Permission To Use The Bot")

  def add_points(id, username, first_name):
    current_points = points.find_one({"_id": id})
    print(current_points)
    the_points = current_points['points']
    print(the_points)
    new_points = int(the_points) + 10
    filter = {"_id": id}
    newvalues = {
      "$set": {
        "username": f"{username}",
        "points": f"{new_points}",
        "first_name": f"{first_name}"
      }
    }
    points.update_one(filter, newvalues)

  @bot.message_handler(func=lambda message: True)
  def all_messages(message):
    # always checking if the user can use the bot
    if str(message.from_user.id) in owners_list:

      # the bot commands
      if message.text == "Add Food":
        bot.send_message(message.from_user.id, "Are You Sure You Want To Add Food ?", reply_markup=keyboard('Confirm'))
        global confirm
        confirm = True
      elif message.text == "No":
        if confirm == True:
          bot.send_message(message.from_user.id, "Cancelled Operation", reply_markup=keyboard('Normal'))
      elif message.text == "Yes":
        if confirm == True:
          times = get_time()
          hours = get_hours()
          minutes = get_minutes()
          next_h = int(hours) + int(time_interval)

          # if the time after adding 12 hours is more than 24 we subtract 24 from it to get the AM time

          if int(next_h) >= 24:
            next_h = abs(int(next_h) - 24)
          next_time = str(next_h) + ":" + str(minutes)

          # setting values to add to the database

          filter = {"_id": 0}
          print(message.from_user.username)
          if message.from_user.username != None:
            newvalues = {
              "$set": {
                "feeder": message.from_user.username,
                "last_time": times,
                "next_time_number": int(next_h),
                "next_time": next_time
              }
            }
          else:
            newvalues = {
              "$set": {
                "feeder": message.from_user.first_name,
                "last_time": times,
                "next_time_number": int(next_h),
                "next_time": next_time
              }
            }
          food.update_one(filter, newvalues)
          # add points
          add_points(message.from_user.id, message.from_user.username, message.from_user.first_name)
          current_user = points.find_one({"_id": message.from_user.id})
          the_points = current_user['points']
          # sending note about this input
          if message.from_user.username != None:
            bot.send_message(message.from_user.id, f"{message.from_user.username} Added Food At {times} Next Food Time in 12 Hours", reply_markup=keyboard("Normal"))
            bot.send_message(message.from_user.id, f"{message.from_user.username} Has Gained 10 😸, Now Has {the_points} 😸")
          else:
            bot.send_message( message.from_user.id, f"{message.from_user.first_name} Added Food At {times} Next Food Time in 12 Hours", reply_markup=keyboard("Normal"))
            bot.send_message( message.from_user.id, f"{message.from_user.first_name} Has Gained 10 😸, Now Has {the_points} 😸")
          confirm = False

      # get the users score

      elif message.text == "Score":
        points_list = []
        for user in owners_list:
          user = int(user)
          the_user = points.find_one({"_id": user})
          user_points = the_user['points']
          username = the_user['username']
          if username != "None" and len(username) > 0:
            result = f"{username}: " + " " + user_points + "😸"
          else:
            first_name = the_user['first_name']
            result = f"{first_name}: " + " " + user_points + "😸"
          points_list.append(result)

        the_message = "\n".join(points_list)
        print(the_message)
        bot.send_message(message.from_user.id, the_message)

      #get last feeding time

      elif message.text == "Last Food Time":

        # the data to get from the database and calculating the remaining time

        stats = food.find_one({"_id": 0})
        last_time = stats['last_time']
        last_feeder = stats['feeder']
        next_hours = stats['next_time_number']
        next_time = stats['next_time']
        now_h = get_hours()
        remain_h = abs(int(next_hours) - int(now_h))

        # if the time difference is more than 12 hours we add 24 to the set time and subtract it from the main time now to get the difference in hours

        if remain_h > 12:
          next_hours = int(next_hours) + 24
          remain_h = abs(int(next_hours) - int(now_h))
          if remain_h >= 24:
            next_hours = int(next_hours) - 24
            remain_h = abs(int(next_hours) - int(now_h))
        # send last time and next time messages

        bot.send_message(
          message.from_user.id,
          f"Last Feeding Time Was {last_time} And Was Done By '{last_feeder}'")
        bot.send_message(
          message.from_user.id,
          f"Next time will Be at {next_time}, which is {remain_h} hours from now"
        )

        # Calculate How Much You're Past The Time

        #if remain_h > time_interval:
        #  past = int(remain_h) - int(time_interval)
        #  bot.send_message(message.from_user.id, f"You're Past The Feeding Time By {past} Hours")

      #Next Feeding Time

      elif message.text == "Next Food Time":
        stats = food.find_one({"_id": 0})
        next_hours = stats['next_time_number']
        next_time = stats['next_time']
        now_h = get_hours()
        remain_h = abs(int(next_hours) - int(now_h))

        # if the time difference is more than 12 hours we add 24 to the set time and subtract it from the main time now to get the difference in hours

        if remain_h > 12:
          next_hours = int(next_hours) + 24
          remain_h = abs(int(next_hours) - int(now_h))
          if remain_h >= 24:
            next_hours = int(next_hours) - 24
            remain_h = abs(int(next_hours) - int(now_h))
        bot.send_message(
          message.from_user.id,
          f"Next time will Be at {next_time}, which is {remain_h} hours from now"
        )

        # Calculate How Much You're Past The Time

        #if remain_h > time_interval:
        #  past = int(remain_h) - int(time_interval)
        #  bot.send_message(message.from_user.id, f"You're Past The Feeding Time By {past} Hours")

        # Don't Send Messages To The bot

      else:
        bot.send_message(
          message.from_user.id,
          "Don't Send Messages To The Bot, Use The Keyboard Please")
        bot.send_photo(
          message.from_user.id,
          "https://i.ibb.co/S6tHBkf/1236-CD33-8219-4378-B8-B8-33-FFA694-D598.jpg"
        )
    else:
      bot.send_message(message.from_user.id,
                       "You Don't Have Permission To Use The Bot")


      # The background loop for the reminder
      #it checks every ten minutes if the current hour matches the hour set in the database
def reminder():
  random_phrase = [
    os.environ["phrase_1"], os.environ["phrase_2"], os.environ["phrase_3"],
    os.environ["phrase_4"]
  ]

  def get_hours():
    time_now = datetime.now()
    hours = int(time_now.strftime("%H"))
    accurate = hours + int(time_zone)
    return accurate

  while (True):
    feeding = food.find_one({"_id": 0})
    next_time = feeding['next_time_number']
    now = get_hours()
    if int(now) == (next_time):
      for i in owners_list:
        phrase = random.choice(random_phrase)
        bot.send_message(
          i, f"it's {next_time}, {phrase}, please add food to {cat_name}")
    time.sleep(600)


# running the bot and the reminder
background_loop = threading.Thread(name='reminder',
                                   daemon=True,
                                   target=reminder)
the_main = threading.Thread(name='main', target=main_bot)

background_loop.start()
the_main.start()
bot.infinity_polling()
keep_alive.keep_alive()
