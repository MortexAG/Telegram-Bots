import os
import requests
import telebot
import keep_alive

BOT_API = os.environ['BOT_KEY']

bot = telebot.TeleBot(BOT_API)
@bot.message_handler(commands=['start', 'help'])
# The Help And Start Commands
def help(message):
  bot.send_message(message.chat.id, "use /mecca or /cairo or /send_location")
# Get Mecca Weather Command
@bot.message_handler(commands=['mecca'])
def mecca(message):
  try:
    lat = 21.455841422340242
    lng = 39.87942219775681
    url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true".format(lat, lng)
    response = requests.get(url)
    data = response.json()
    f = data['current_weather']['temperature']
    c = round(f)
    bot.send_message(message.chat.id, "Tempreture in Mecca now is Around ({} C°)".format(c))
  except:
    bot.send_message(message.chat.id, "Sorry The Bot is Not Working Now, Try Later or Send To The Maker For Debugging")

# Get Cairo Weather Command
@bot.message_handler(commands=['cairo'])
def cairo(message):
  try:
    lat = 30.046321259557125
    lng = 31.244240957699272
    url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true".format(lat, lng)
    response = requests.get(url)
    data = response.json()
    f = data['current_weather']['temperature']
    celsius = round(f)
    bot.send_message(message.chat.id, "Tempreture in Cairo now is Around ({} C°)".format(celsius))
  except:
    bot.send_message(message.chat.id, "Sorry The Bot is Not Working Now, Try Later or Send To The Maker For Debugging")
@bot.message_handler(commands=['send_location'])
def coordinates(message):
  bot.send_message(message.chat.id, "Send The Location Please")
  @bot.message_handler(func=lambda message: True,       content_types='location')
  def location(message):
    try:
      message = message
      # extract the exact location from the location sent
      lat = message.location.latitude
      lng = message.location.longitude
      # run the api as usual
      url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true".format(lat, lng)
      response = requests.get(url)
      data = response.json()
      f = data['current_weather']['temperature']
      celsius = round(f)
      bot.send_message(message.chat.id, "Tempreture in This Location now is Around ({} C°)".format(celsius))

    except:
      bot.send_message(message.chat.id, "Sorry The Bot is Not Working Now, Try Later or Send To The Maker For Debugging")


bot.infinity_polling()
keep_alive.keep_alive()
