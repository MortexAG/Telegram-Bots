import os
import telebot
import keep_alive
import pymongo
from pymongo import MongoClient
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


BOT_API = os.environ['BOT_API']
mongo_connect = os.environ['mongo_connect']
client = MongoClient(mongo_connect)
db = client['grocery_bot_2']
collection = db['items']
# owners list
owner_1 = int(os.environ['owner_1'])
owner_2 = int(os.environ['owner_2'])


owners_list = [owner_1, owner_2]

bot = telebot.TeleBot(BOT_API)

# Create keyboard buttons
add_button = KeyboardButton('/add')
list_button = KeyboardButton('/list')
fulfill_button = KeyboardButton('/fulfill')

# Create the keyboard markup
keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_markup.add(add_button)
keyboard_markup.add(list_button)
keyboard_markup.add(fulfill_button)

def delete_fulfilled_items():
    count = collection.count_documents({'fulfilled': True})
    if count == 0:
        print('No fulfilled items found.')
    else:
        collection.delete_many({'fulfilled': True})
        print(f'Deleted {count} fulfilled items.')
  
delete_fulfilled_items()

# Handle the /start command to send the keyboard
@bot.message_handler(commands=['start'])
def send_keyboard(message):
  if int(message.from_user.id) not in owners_list:
    bot.send_message(message.from_user.id, "You Don't Have Permission To Use This Bot")
  else:
    bot.send_message(message.chat.id, 'Welcome! What would you like to do?', reply_markup=keyboard_markup)

# Handle the /add command to add items to the list
@bot.message_handler(func=lambda message: message.text == '/add', content_types=['text'])
def add_item(message):
  if int(message.from_user.id) not in owners_list:
      bot.send_message(message.from_user.id, "You Don't Have Permission To Use This Bot")
  else:
      bot.send_message(message.chat.id, 'What item would you like to add?')
      bot.register_next_step_handler(message, add_item_to_database)

def add_item_to_database(message):
    item = message.text
    collection.insert_one({'name': item, 'fulfilled': False})
    bot.send_message(message.chat.id, f'Added {item} to the list', reply_markup=keyboard_markup)

# Handle the /list command to retrieve the list of items
@bot.message_handler(func=lambda message: message.text == '/list', content_types=['text'])
def list_items(message):
  if int(message.from_user.id) not in owners_list:
    bot.send_message(message.from_user.id, "You Don't Have Permission To Use This Bot")
  else:
    items = collection.find()
    missing = []
    fulfilled = []
    for item in items:
        if item['fulfilled']:
            fulfilled.append(item['name'])
        else:
            missing.append(item['name'])

    if not missing:
        bot.send_message(message.chat.id, 'All items have been fulfilled!', reply_markup=keyboard_markup)
    else:
        keyboard_markup_items = ReplyKeyboardMarkup(resize_keyboard=True)
        for item in missing:
            keyboard_markup_items.add(KeyboardButton(item))
        keyboard_markup_items.add(KeyboardButton('Back to Main Menu'))
        bot.send_message(message.chat.id, 'Missing items:', reply_markup=keyboard_markup_items)
        bot.register_next_step_handler(message, select_missing_item)

def select_missing_item(message):
    if message.text == 'Back to Main Menu':
        bot.send_message(message.chat.id, 'What would you like to do?', reply_markup=keyboard_markup)
    else:
        item = message.text
        bot.send_message(message.chat.id, f'{item} is still missing', reply_markup=keyboard_markup)

@bot.message_handler(func=lambda message: message.text == '/fulfill', content_types=['text'])
def fulfill_item(message):
  if int(message.from_user.id) not in owners_list:
    bot.send_message(message.from_user.id, "You Don't Have Permission To Use This Bot")
  else:
    items = list(collection.find({'fulfilled': False}))
    if not items:
        bot.send_message(message.chat.id, 'All items have been fulfilled!', reply_markup=keyboard_markup)
    else:
        keyboard_markup_items = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for item in items:
            keyboard_markup_items.add(KeyboardButton(item['name']))
        keyboard_markup_items.add(KeyboardButton('Back to Main Menu'))
        bot.send_message(message.chat.id, 'What item would you like to mark as fulfilled?', reply_markup=keyboard_markup_items)
        bot.register_next_step_handler(message, select_fulfilled_item, items)

def select_fulfilled_item(message, items):
    if message.text == 'Back to Main Menu':
        bot.send_message(message.chat.id, 'What would you like to do?', reply_markup=keyboard_markup)
    else:
        item = message.text
        collection.update_one({'name': item}, {'$set': {'fulfilled': True}})
        delete_fulfilled_items()
        bot.send_message(message.chat.id, f'{item} has been marked as fulfilled', reply_markup=keyboard_markup)
        fulfill_item(message)  # return to the fulfill menu after marking an item as fulfilled

# Run the bot
      
bot.infinity_polling()
keep_alive.keep_alive()
