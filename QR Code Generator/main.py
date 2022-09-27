import os
import telebot
import requests
import glob
import keep_alive

BOT_API = os.environ["BOT_API"]
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(BOT_API)
state = "inactive"
def empty_dir():
  for filename in glob.glob('./qr-image/*'):
            generated_qr = filename
            os.remove(generated_qr)
def qr_create(message):
          bot.send_message(message.chat.id, "Text Recieved Generating The QR Code Now Please Wait")
          qr_text = message.text
          url ="http://api.qrserver.com/v1/create-qr-code/?data={}&size=500x500".format(qr_text)
          response = requests.get(url)
          file = open("./qr-image/result.jpg", "wb")
          file.write(response.content)
          file.close()
          qr_result = open("./qr-image/result.jpg", "rb")
          bot.send_photo(message.chat.id, qr_result)
          empty_dir()  

@bot.message_handler(commands=["start", "help", "keyboard"])
def start_message(message):
  bot.send_message(message.chat.id, 'Welcome To The QR Code Generator Bot Send The Text Directly In The Chat To Convert It To A QR Code')

  
@bot.message_handler(func=lambda message:True)
def all_messages(message):
  qr_create(message)
  
bot.infinity_polling()
keep_alive.keep_alive()
