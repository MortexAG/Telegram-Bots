import time
from datetime import datetime
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
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
    global id_clock 
    id_clock = str(clock_id)
    global clock_state
    clock_state = "active"
    while (True):
        now = datetime.now()
        timenow = now.strftime("%H:%M:%S")
        bot.edit_message_text(timenow, message.from_user.id, message.message_id+2)
        time.sleep(1)


def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=2)
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
        markup.add(KeyboardButton("✅Done"))
        markup.add(KeyboardButton(""))
        markup.add(KeyboardButton(""))
    elif key_type == 'first page':
        markup.add(KeyboardButton("Say Hi"))
        markup.add(KeyboardButton("Go Back"))
        markup.add(KeyboardButton("✅Done"))
        markup.add()
        markup.add()
    return markup

@bot.message_handler(commands=["start"])
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
        bot.send_message(message.from_user.id, 'welcome second year', reply_markup=keyboard('second page'))
    elif message.text == 'Clock':
        bot.send_message(message.from_user.id, "clock", reply_markup=keyboard('Clock'))
    elif message.text == 'Activate Clock':
        global clock_state
        if clock_state == "inacitve":
            bot.send_message(message.from_user.id, "Clock Activated")
            clock(message)
        elif clock_state == "active":
            bot.send_message(message.from_user.id, "There's A Currently Active Clock, Delete it First")
    elif message.text == 'Delete Clock':
        if clock_state == "active":
            bot.delete_message(message.from_user.id, id_clock)
            clock_inactivate()
            bot.send_message(message.from_user.id, "Clock Deleted")
        elif clock_state == "inacitve":
            bot.send_message(message.from_user.id, "There Are No Active Clocks To Stop")
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
    else:
        bot.send_message(message.chat.id,message.text)


bot.infinity_polling()
