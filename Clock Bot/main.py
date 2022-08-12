import time
import datetime
from datetime import datetime
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import keep_alive
BOT_API = os.environ["BOT_API"]
bot = telebot.TeleBot(BOT_API)

clock_state = "inacitve"
def clock_inactivate():
    global clock_state
    clock_state = "inacitve"

def clock(message):
    now_first = datetime.now()
    timenow_first = now_first.strftime("%H:%M:%S")
    bot.send_message(message.from_user.id, timenow_first)
    time.sleep(1)
    clock_id = (message.message_id+2)
    activated_message = (message.message_id+1)
    global clock_activated_id
    clock_activated_id = str(activated_message)
    global id_clock 
    id_clock = str(clock_id)
    global clock_state
    clock_state = "active"
    while (True):
        now = datetime.now()
        timenow = now.strftime("%H:%M:%S")
        bot.edit_message_text(timenow, message.from_user.id, message.message_id+2)
        time.sleep(1)

def delete_clock(message):
    bot.delete_message(message.from_user.id, clock_activated_id)
    bot.delete_message(message.from_user.id, id_clock)


def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyobard=True)
    if key_type == "Normal":
        row = [KeyboardButton('first page')]
        markup.add(*row)
        markup.add(KeyboardButton('second page'))
        markup.add(KeyboardButton('Clock'))
        markup.add(KeyboardButton("Delete This"))
        markup.add(KeyboardButton("🔙Delete"),KeyboardButton("✅Done"))
        markup.add()
    elif key_type == 'Clock':
        markup.add(KeyboardButton('Activate Clock'))
        markup.add(KeyboardButton('Delete Clock'))
        markup.add(KeyboardButton('Clock State'))
        markup.add(KeyboardButton("Go Back"))
    elif key_type == 'second page':
        row = [KeyboardButton( 'nothing here')]
        markup.add(*row)
        row = [KeyboardButton('Go Back')]
        markup.add(*row)
    elif key_type == 'first page':
        markup.add(KeyboardButton("Say Hi"))
        markup.add(KeyboardButton("My Username"))
        markup.add(KeyboardButton("My ID"))
        markup.add(KeyboardButton("Go Back"))

    return markup

@bot.message_handler(commands=["start", "keyboard"])
def start_message(message):
    bot.send_message(message.chat.id,"You can use the keyboard",reply_markup=keyboard())

@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if message.text == "✅Done":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Done with Keyboard",reply_markup=markup)
    elif message.text == 'first page':
        bot.send_message(message.from_user.id, 'going to first page', reply_markup=keyboard('first page'))
    elif message.text == 'second page':
        bot.send_message(message.from_user.id, 'welcome to second page', reply_markup=keyboard('second page'))
    elif message.text == 'Clock':
        bot.send_message(message.from_user.id, "Clock", reply_markup=keyboard('Clock'))
    elif message.text == 'Activate Clock':
        global clock_state
        if clock_state == "inacitve":
            bot.send_message(message.from_user.id, "Clock Activated")
            clock(message)
        elif clock_state == "active":
            clock_inactivate()
            delete_clock(message)
            bot.send_message(message.from_user.id, "Clock Activated")
            clock(message)
    elif message.text == 'Delete Clock':
        if clock_state == "active":
            delete_clock(message)
            clock_inactivate()
            bot.send_message(message.from_user.id, "Clock Deleted")
        elif clock_state == "inacitve":
            bot.send_message(message.from_user.id, "There Are No Active Clocks To Delete")
    elif message.text == "Clock State":
        bot.send_message(message.from_user.id, clock_state)
    elif message.text == "Go Back":
        bot.send_message(message.from_user.id, "Going Back", reply_markup=keyboard("Normal"))
    elif message.text == "Normal":
        bot.send_message(message.from_user.id,"Normal Keyboard",reply_markup=keyboard("Normal"))
    elif message.text == "🔙Delete":
        bot.delete_message(message.from_user.id,message.message_id)
    elif message.text == "Delete This":
        bot.send_message(message.from_user.id, "This will be deleted in 1s")
        time.sleep(1)
        bot.delete_message(message.from_user.id,message.message_id+1)
    elif message.text == "Say Hi":
        bot.send_message(message.from_user.id, "Hi"+" "+ message.from_user.first_name+" "+message.from_user.last_name)
    elif message.text == "My Username":
        bot.send_message(message.from_user.id,"@"+message.from_user.username)
    elif message.text == "My ID":
        bot.send_message(message.from_user.id,message.from_user.id)
    else:
        bot.send_message(message.chat.id,message.text)

bot.infinity_polling()
keep_alive.keep_alive()
