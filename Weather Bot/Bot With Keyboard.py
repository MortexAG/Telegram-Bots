import os
import requests
import telebot
import keep_alive
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_API = os.environ['BOT_KEY']

bot = telebot.TeleBot(BOT_API)
## The Functions Are Here ##
# The Send Locations Function
def send_location():
  @bot.message_handler(func=lambda message: True,       content_types='location')
  def location(message):
    try:
            message = message
            # extract the exact location from the location sent
            lat = message.location.latitude
            lng = message.location.longitude
            # run the api as usual
            url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true".format(
                lat, lng)
            response = requests.get(url)
            data = response.json()
            f = data['current_weather']['temperature']
            celsius = round(f)
            bot.send_message(
                message.from_user.id,
                "Tempreture in This Location Now is Around, ({} C°)".format(celsius))

    except:
            bot.send_message(
                message.from_user.id,
                "Sorry The Bot is Not Working Now, Try Later or Send To The Maker For Debugging"
            )
# The Mecca Location Function
def mecca(message):
    try:
        lat = 21.455841422340242
        lng = 39.87942219775681
        url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true".format(
            lat, lng)
        response = requests.get(url)
        data = response.json()
        f = data['current_weather']['temperature']
        c = round(f)
        bot.send_message(message.chat.id,
                         "Tempreture in Mecca now is Around ({} C°)".format(c))
    except:
        bot.send_message(
            message.chat.id,
            "Sorry The Bot is Not Working Now, Try Later or Send To The Maker For Debugging"
        )
      
  # The Cairo Weather Function
def cairo(message):
    try:
        lat = 30.046321259557125
        lng = 31.244240957699272
        url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true".format(
            lat, lng)
        response = requests.get(url)
        data = response.json()
        f = data['current_weather']['temperature']
        celsius = round(f)
        bot.send_message(
            message.chat.id,
            "Tempreture in Cairo now is Around ({} C°)".format(celsius))
    except:
        bot.send_message(
            message.chat.id,
            "Sorry The Bot is Not Working Now, Try Later or Send To The Maker For Debugging"
        )

  # The Bot Keyboard
def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if key_type == "Normal":
        row = [KeyboardButton('Send Location')]
        markup.add(*row)
        markup.add(KeyboardButton('Preset Locations'))
        markup.add(KeyboardButton('About'))
        markup.add(KeyboardButton('Exit Keyboard'))
    elif key_type == "Preset Locations":
      markup.add(KeyboardButton('Mecca'))
      markup.add(KeyboardButton('Cairo'))
      markup.add(KeyboardButton('Go Back'))

    return markup

@bot.message_handler(commands=['help'])
# The Help And Start Commands
def help(message):
    bot.send_message(message.chat.id, "use /start or /keyboard to open the set of commands")

@bot.message_handler(commands=['start', 'keyboard'])
def start(message):
  bot.send_message(message.chat.id,"You can use the keyboard",reply_markup=keyboard())
      

# The Keyboard Functions

@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if message.text == "Exit Keyboard":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Done with Keyboard",reply_markup=markup)
    elif message.text == "Send Location":
      bot.send_message(message.chat.id, "Send The Location Please")
      send_location()
    elif message.text == 'Preset Locations':
      bot.send_message(message.from_user.id, message.text, reply_markup=keyboard('Preset Locations'))
    elif message.text == 'Mecca':
      bot.send_message(message.from_user.id, message.text)
      mecca(message)
    elif message.text == 'Cairo':
      bot.send_message(message.from_user.id, message.text)
      cairo(message)
    elif message.text == 'Go Back':
      bot.send_message(message.from_user.id, 'Going back', reply_markup=keyboard('Normal'))
    elif message.text == "About":
      bot.send_message(message.from_user.id, "This Bot Was Created by MortexAG")
      bot.send_message(message.from_user.id, "You Can Use /start or /keyboard To The Start The Bot's Command List")
      bot.send_message(message.from_user.id, "Please Don't Spam The Buttons, Note That The Tempreature Sent By This Bot Is Not Very Accurate")
    else:
      bot.send_message(message.from_user.id, "Unidentified Command, Please Use The Keyboard or The Commands and Don't Send Direct Messages To The Bot, You May Need To Restart The Bot")
      
bot.infinity_polling()
keep_alive.keep_alive()
