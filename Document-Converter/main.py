import os
import telebot
import convertapi
import glob
import PIL
from PIL import Image
import keep_alive
BOT_API = os.environ["BOT_API"]
API_SECRET = os.environ['API_SECRET']
bot = telebot.TeleBot(BOT_API)

# Path Checks For The Important Directories

if os.path.exists("./converted"):
  pass
else:
  os.mkdir("./converted")
  
if os.path.exists("./downloaded"):
  pass
else:
  os.mkdir("./downloaded")

if os.path.exists("./result"):
  pass
else:
  os.mkdir("./result")
  
if os.path.exists("./images"):
  pass
else:
  os.mkdir("./images")
if os.path.exists("./images/photos"):
  pass
else:
  os.mkdir("./images/photos")

def empty_converted():
  for filename in glob.glob('converted/*'):
    file_converted_delete = filename
    os.remove(file_converted_delete)
def empty_downloaded():
  for filename in glob.glob('downloaded/*'):
    file_downloaded_delete = filename
    os.remove(file_downloaded_delete)

def empty_images():
  for filename in glob.glob('images/photos/*'):
    file_downloaded_delete = filename
    os.remove(file_downloaded_delete)

def empty_result():
  for filename in glob.glob('result/*'):
    file_downloaded_delete = filename
    os.remove(file_downloaded_delete)


empty_images()
empty_result()

empty_converted()
empty_downloaded()


def word_to_pdf():
  convertapi.api_secret = API_SECRET
  convertapi.convert('pdf', {
    'File': "./downloaded/"+file_name
}, from_format = 'docx').save_files('./converted')
def pdf_to_word():
  convertapi.api_secret = API_SECRET
  convertapi.convert('word', {
    'File': "./downloaded/"+file_name
}, from_format = 'pdf').save_files('./converted')

def ppt_to_pdf():
  convertapi.api_secret = API_SECRET
  convertapi.convert('pdf', {
    'File': "./downloaded/"+file_name
}, from_format = 'ppt').save_files('./converted')
def pptx_to_pdf():
  convertapi.api_secret = API_SECRET
  convertapi.convert('pdf', {
    'File': "./downloaded/"+file_name
}, from_format = 'pptx').save_files('./converted')

def powerpoint_to_pdf():
  try:
    ppt_to_pdf()
  except:
    pptx_to_pdf()
  

def get_downloaded_file():
  bot.get_file()

def one_image_to_pdf():

  names = 0
  for i in glob.glob("./images/photos/*"):

    #Open The Each Image
    image_open = Image.open(i)

    #Convert Each One To RGB
    rgb_image = image_open.convert("RGB")

    #Naming Order For Pdf
    names += 1

    #Convert each image to pdf
    rgb_image.save(f"./result/result.pdf")
    empty_images()

@bot.message_handler(commands=["start", "keyboard"])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Send A Word Or A PDF Or A Powerpoint Document Directly in This Chat To Convert It")


@bot.message_handler(commands=['clear'])
def replying(message):
  bot.send_message(message.chat.id, "Cleared All Downloaded Files in The Bot's Storage")
  empty_converted()
  empty_downloaded()
@bot.message_handler(content_types=['document'])
def document(message):
    
    print ('message.document =', message.document)
    fileID = message.document.file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    global file_name
    file_name = message.document.file_name
    print(file_name)
    file_downloaded = file_name
    file_type = message.document.mime_type
    with open("./downloaded/"+file_downloaded, 'wb') as new_file:
        new_file.write(downloaded_file)
      
    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      bot.reply_to(message, "Word Document Recieved")
      word_to_pdf()
      bot.send_message(message.chat.id, "Word Converted To PDF")
      for filename in glob.glob('converted/*'):
        pdf_converted = open(filename, "rb")
        bot.send_document(message.chat.id, pdf_converted)
        empty_converted()
        empty_downloaded()
    elif file_type == "application/pdf":
      bot.reply_to(message, "PDF Document Recieved")
      pdf_to_word()
      bot.send_message(message.chat.id, "PDF Converted To Word")
      for filename in glob.glob('converted/*'):
        word_converted = open(filename, "rb")
        bot.send_document(message.chat.id, word_converted)
        empty_converted()
        empty_downloaded()
    elif file_type in("application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.ms-powerpoint"):
        bot.reply_to(message, "Powerpoint Document Recieved")
        powerpoint_to_pdf()
        for filename in glob.glob('converted/*'):
          powerpoint_converted = open(filename, 'rb')
          bot.send_message(message.chat.id, "Powerpoint Converted To PDF")
          bot.send_document(message.chat.id, powerpoint_converted)
          empty_converted()
          empty_downloaded()
                
    else:
        print(file_type)
        bot.send_message(message.chat.id, file_type)
        bot.send_message(message.chat.id, "Please Send PDF or Word Documents Only")
        empty_converted()
        empty_downloaded()

@bot.message_handler(content_types=['photo'])
def image_convert(message):
    bot.reply_to(message, "Image Recieved, Converting To PDF")

    fileID = message.photo[-1].file_id
    #print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    file_new_name = file_info.file_path.replace("./images/", "")
    #print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"./images/{file_new_name}", 'wb') as new_file:
      new_file.write(downloaded_file)
    one_image_to_pdf()
    final_pdf = open("./result/result.pdf", "rb")
    bot.send_message(message.from_user.id, "Image Converted To Pdf")
    bot.send_document(message.from_user.id, final_pdf)
    empty_images()
    empty_result()


bot.infinity_polling()
keep_alive.keep_alive()
