import os
import requests
import telebot
import keep_alive

BOT_API = os.environ['BOT_KEY']

WEATHER_API = os.environ['WEATHER_API']

headers = {
    'x-api-key': WEATHER_API,
    'Content-type': "application/json"
    }

bot = telebot.TeleBot(BOT_API)
@bot.message_handler(commands=['start', 'help'])
# The Help And Start Commands
def help(message):
  bot.send_message(message.chat.id, "use /mecca or /cairo or /send_location")
# Get Mecca Weather Command
@bot.message_handler(commands=['mecca'])
def mecca(message):
  lat = 21.455841422340242
  lng = 39.87942219775681
  url = "https://api.ambeedata.com/weather/latest/by-lat-lng?lat={}&lng={}".format(lat, lng)
  response = requests.get(url, headers=headers)
  data = response.json()
  f = data['data']['temperature']
  celsius = (f-32)*(5/9)
  c = round(celsius)
  weather = data['data']['summary']
  bot.send_message(message.chat.id, "Tempreture in Mecca now is Around ({} C°)".format(c))
  bot.send_message(message.chat.id, "The Weather is ({})".format(weather))

# Get Cairo Weather Command
@bot.message_handler(commands=['cairo'])
def cairo(message):
  lat = 30.046321259557125
  lng = 31.244240957699272
  url = "https://api.ambeedata.com/weather/latest/by-lat-lng?lat={}&lng={}".format(lat, lng)
  response = requests.get(url, headers=headers)
  data = response.json()
  f = data['data']['temperature']
  c = (f-32)*(5/9)
  celsius = round(c)
  weather = data['data']['summary']
  bot.send_message(message.chat.id, "Tempreture in Cairo now is Around ({} C°)".format(celsius))
  bot.send_message(message.chat.id, "The Weather is ({})".format(weather))

@bot.message_handler(commands=['send_location'])
def coordinates(message):
  bot.send_message(message.chat.id, "Send The Location Please")
  @bot.message_handler(func=lambda message: True,       content_types='location')
  def location(message):
    message = message
    # extract the exact location from the location sent
    lat = message.location.latitude
    lng = message.location.longitude
    # run the api as usual
    url = "https://api.ambeedata.com/weather/latest/by-lat-lng?lat={}&lng={}".format(lat, lng)
    response = requests.get(url, headers=headers)
    data = response.json()
    f = data['data']['temperature']
    c = (f-32)*(5/9)
    celsius = round(c)
    weather = data['data']['summary']
    bot.send_message(message.chat.id, "Tempreture in This Location now is Around ({} C°)".format(celsius))
    bot.send_message(message.chat.id, "The Weather in This Location is ({})".format(weather))


bot.infinity_polling()
keep_alive.keep_alive()
