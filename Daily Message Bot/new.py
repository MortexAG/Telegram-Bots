import telebot
import datetime 
from datetime import datetime
import os
import keep_alive
import mysql.connector
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


BOT_TOKEN = os.environ['BOT_API']
bot = telebot.TeleBot(BOT_TOKEN)

db_host = os.environ['db_host']
db_pass = os.environ['db_pass']
db_user = os.environ['db_user']

mydb = mysql.connector.connect (
  host = db_host,
  user = db_user,
  password = db_pass,
  database = db_user
)
cursor = mydb.cursor()

def get_current_time():
  times = datetime.now()
  now = times.strftime("%Y-%m-%d, %H:%M:%S")
  return now
  
daytime = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
setting_now = "unavilable"
def time_undone():
  global time_is_done
  time_is_done = "undone"
time_undone()
def time_done():
  global time_is_done
  time_is_done = "done"
def custom_inactive():
  global custom_state
  custom_state = "inactive"
custom_inactive()
def custom_active():
  global custom_state
  custom_state = "active"
def unsub_inactive():
  global unsub_confirm
  unsub_confirm = "none"
unsub_inactive()
def unsub_active():
  global unsub_confirm
  unsub_confirm = "active"
  
def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    if key_type == "Normal":
      markup.add(KeyboardButton('Subscribe'))
      markup.add(KeyboardButton("Show My Message"))
      markup.add(KeyboardButton('Unsubscribe'))
    elif key_type == "Subscribe":
      markup.add(KeyboardButton("Choose Time"))
      markup.add(KeyboardButton("Choose Message"))
      markup.add(KeyboardButton("Go Back"))
    elif key_type == "Choose Time":
      row = daytime
      markup.add(*row)
      markup.add(KeyboardButton("Back"))
    elif key_type == "Choose Message":
      markup.add(KeyboardButton("Custom Message"))
      markup.add(KeyboardButton("Default Message"))
      markup.add(KeyboardButton("Back"))
    elif key_type == "Unsubscribe":
      markup.add(KeyboardButton("Confirm Unsubscribe"))
      markup.add(KeyboardButton("Cancel"))

    return markup
  

@bot.message_handler(commands=['start'])
def start_new(message):
  try :
    sql_user = f"""SELECT * FROM `gm_bot_users` WHERE userid = {message.from_user.id}"""
    cursor.execute(sql_user)
    for comp in cursor:
      ono = comp[1]
    bot.send_message(message.from_user.id, f"Welcome Back {ono}")
    bot.send_message(message.from_user.id,"Welcome To The Daily Message Bot Register An Account And Choose The Time And Message To Be Sent Daily, NOTE That The Bot Is Not Accurate As The Message Can Be Recieved Any Time During The Hour You Will Decide", reply_markup=keyboard())
  except :
    bot.send_message(message.from_user.id,"Welcome To The Bot, This Bot Can Send A Message Daily In The Same One Hour Period, To Start using The Bot Please Use The Following Command /subscribe, To Stop Recieving Daily Messages Use /unsubscribe", reply_markup=keyboard())
    now = get_current_time()
    sql_add_new = f""" INSERT INTO `gm_bot_users` (id, username, userid, join_date) VALUES (0, '{message.from_user.first_name+' '+message.from_user.last_name}', '{message.from_user.id}', '{now}')"""
    cursor.execute(sql_add_new)
    mydb.commit()

@bot.message_handler(commands=['keyboard'])
def enable_keyboard(message):
  bot.send_message(message.from_user.id, "Keyboard Activated", reply_markup=keyboard())

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.from_user.id, "Welcome To The Daily Message Bot Register An Account And Choose The Time And Message To Be Sent Daily, NOTE That The Bot Is Not Accurate As The Message Can Be Recieved Any Time During The Hour You Will Decide")


def check_sub(message):
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      print("hi")
def subscribe(message):
  try :
    sql_subscribed = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
    cursor.execute(sql_subscribed)
    for comp in cursor:
      sub_id = comp[2].strip()
    bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
    bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
  except:
    bot.send_message(message.from_user.id, message.text, reply_markup=keyboard('Subscribe'))

def insert_sub(message):
  now = get_current_time()
  sql_subscribe = f"""INSERT INTO `gm_bot_subscribers` (id, username, userid, subscription_state, subscription_date, message,message_time,  message_state) VALUES (0, '{message.from_user.first_name+' '+message.from_user.last_name}',' {message.from_user.id}', 'subscribed','{now}', '{message.text}','{msg_time}' ,  'not_sent') """
  cursor.execute(sql_subscribe)
  mydb.commit()

@bot.message_handler(func=lambda message:True)
def all_messages(message):
  if message.text == "✅Done":
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id,"Done with Keyboard",reply_markup=markup)
  elif message.text == "Subscribe":
    subscribe(message)
    global state
    state = "subscribe"
  elif message.text == "Choose Time":
    ## Checking
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      bot.send_message(message.from_user.id, "Send The Time You Want To Recieve The Daily Message", reply_markup = keyboard('Choose Time'))
      global setting_now
      setting_now = "available"
  elif message.text == "Back" and setting_now == "availabe":
    bot.send_message(message.from_user.id, "Going Back", reply_markup = keyboard('Subscribe'))
    setting_now = "unavilable"
  elif message.text in daytime and setting_now == "available":
    ### Checking
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      def time_msg(message):
        global msg_time
        msg_time = message.text
        global time_is_done
        bot.send_message(message.from_user.id, f"The Time is {message.text} GMT in 24hr Format", reply_markup = keyboard('Subscribe'))
        time_done()
      time_msg(message)
      setting_now = "unavilable"
  elif message.text == "Choose Message":
    ###checking
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      state = 'choose_message'
      if time_is_done == "done":
        bot.send_message(message.from_user.id, "Please Choose One Of The Message Options", reply_markup=keyboard('Choose Message'))
      else:
        bot.send_message(message.from_user.id, "Please Choose The Time First")
  elif message.text == "Default Message":
    ### Checking
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      if time_is_done == "done":
        global default_msg
        empty = f" {message.from_user.last_name}"
        default_msg = (f"Good Morning {message.from_user.first_name}{empty} The Time Now is {msg_time}, Have A Nice Day!")
        bot.send_message(message.from_user.id, f"You Are Now Subscribed And Will Recieve The Default Daily Message Everyday at {msg_time} GMT , 24hr Format, To Change The Time Unsubscribe Then Subscribe Again")
        bot.send_message(message.from_user.id, f"The Default Daily Message is, \n{default_msg}", reply_markup = keyboard('Normal'))
        time_undone()
        now = get_current_time()
        sql_subscribe_default = f"""INSERT INTO `gm_bot_subscribers` (id, username, userid, subscription_state, subscription_date, message,message_time,  message_state) VALUES (0, '{message.from_user.first_name+' '+message.from_user.last_name}',' {message.from_user.id}', 'subscribed','{now}', '{default_msg}','{msg_time}' ,  'not_sent') """
        cursor.execute(sql_subscribe_default)
        mydb.commit()
      else:
        bot.send_message(message.from_user.id, "Please Choose The Time First")
  elif message.text == "Custom Message":
    ###Checking
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      if time_is_done == "done":
        bot.send_message(message.from_user.id, "Send The Custom Message You Want To Recieve Daily")
        custom_active()
      else:
        bot.send_message(message.from_user.id, "Please Choose The Time First")
  elif message.text != "Choose Message" and custom_state == "active":
    ###checking
    try :
      sql_check = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_check)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're Already Subscribed")
      bot.send_message(sub_id, "If You Want To Change Anything Unsubsribe Then Subscribe Again")
    except:
      custom_msg = message.text
      bot.send_message(message.from_user.id, f"You Are Now Subscribed And Will Recieve Your Custom Daily Message Everyday at {msg_time} GMT , 24hr Format, To Change The Time Or The Message Unsubscribe Then Subscribe Again")
      bot.send_message(message.from_user.id, f"Your Custom Daily Message is, \n{custom_msg}")
      time_undone()
      custom_inactive()
      insert_sub(message)
  elif message.text == "Go Back":
    bot.send_message(message.from_user.id, "Going back", reply_markup =keyboard('Normal'))
  elif message.text == "Back":
    bot.send_message(message.from_user.id, "Going back", reply_markup =keyboard('Subscribe'))
  elif message.text == "Unsubscribe":
    ### Checking
    try :
        sql_check_sub = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
        cursor.execute(sql_check_sub)
        for comp in cursor:
          sub_id = comp[2].strip()
        bot.send_message(sub_id, f"Hello {comp[1].strip()}, You're About To Unsubscribe", reply_markup =keyboard('Unsubscribe'))
        unsub_active()
    except:
        bot.send_message(message.from_user.id, "You're Not Subscribed")
  elif message.text == "Confirm Unsubscribe" and unsub_confirm == "active":
    sql_unsubscribe = f"""DELETE FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
    cursor.execute(sql_unsubscribe)
    mydb.commit()
    bot.send_message(message.from_user.id, "Unsubscribed Successfully", reply_markup = keyboard("Normal"))
    unsub_inactive()
  elif message.text == "Cancel" and unsub_confirm == "active":
    bot.send_message(message.from_user.id, "Operation Cancelled", reply_markup = keyboard('Normal'))
    unsub_inactive()

  elif message.text == "Show My Message":
    try :
      sql_subscribed = f"""SELECT * FROM `gm_bot_subscribers` WHERE userid = {message.from_user.id}"""
      cursor.execute(sql_subscribed)
      for comp in cursor:
        sub_id = comp[2].strip()
      bot.send_message(sub_id, f"Hello {comp[1].strip()}, Your Daily Message is")
      bot.send_message(sub_id, comp[5].strip())
    except:
      bot.send_message(message.from_user.id, "You're Not Subscribed")
    
print("The Bot Is Running")
bot.infinity_polling()
keep_alive.keep_alive()
