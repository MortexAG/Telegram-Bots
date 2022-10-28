import telebot
import os
import requests
import glob
import keep_alive
BOT_API = os.environ["BOT_API"]
Access_Token = os.environ['Access Token']
bot = telebot.TeleBot(BOT_API)

def empty_images():
  for filename in glob.glob('images/*'):
    file_downloaded_delete = filename
    os.remove(file_downloaded_delete)
empty_images()

def upload_image(message):
  url = "https://api.imgur.com/3/upload"
  payload={}
  files=[
        ('image',('file',open(f'./images/{message}','rb'),'application/octet-stream'))
        ]
  headers = {
          'Authorization': f'Client-ID {Access_Token}'
        }

  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  result = response.json()
  #print(result)
  #print(result["data"]["link"])
  return result["data"]["link"]

@bot.message_handler(commands=["start", 'help'])
def start(message):
  bot.send_message(message.from_user.id, "To Upload Any Image Send It Directly In This Chat And You Will Recieve A Direct Link For It")

@bot.message_handler(content_types = ['photo'])
def image_upload(message):
  bot.reply_to(message, "Image Recieved Please Wait For The Upload")
  try:
    fileID = message.photo[-1].file_id
    #print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    file_new_name = file_info.file_path.replace("photos/", "")
    #print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"./images/{file_new_name}", 'wb') as new_file:
      new_file.write(downloaded_file)
    image_link = upload_image(file_new_name)
    bot.send_message(message.from_user.id, "Image Was Uplaoded Successfully, This is The Image's Link")
    bot.send_message(message.from_user.id, image_link)
    empty_images()
    print("An Image Was Recieved And Uploaded Successfully")
  except:
    empty_images()
    bot.send_message(message.from_user.id, "There Was An Error In Image Upload Please Try Again, If The Issue Presists Try At Another Time")
    print("An Image Was Recieved And There Was An Error Uploading It")
@bot.message_handler(content_types = ['text'])
def no_text(message):
  bot.send_message(message.from_user.id, "Please Send Only Images To The Chat Or Use The Commands /start , /help")
print("Bot Is Running")
bot.infinity_polling()
keep_alive.keep_alive()
