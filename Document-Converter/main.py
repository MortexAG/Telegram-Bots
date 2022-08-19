import os
import telebot
import convertapi
import glob
import keep_alive
BOT_API = os.environ["BOT_API"]
API_SECRET = os.environ['API_SECRET']
bot = telebot.TeleBot(BOT_API)
def empty_converted():
  for filename in glob.glob('converted/*'):
    file_converted_delete = filename
    os.remove(file_converted_delete)
def empty_downloaded():
  for filename in glob.glob('downloaded/*'):
    file_downloaded_delete = filename
    os.remove(file_downloaded_delete)

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
def get_downloaded_file():
  bot.get_file()

@bot.message_handler(commands=["start", "keyboard"])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Send A Word Or A PDF Document Directly in This Chat To Convert Them")


@bot.message_handler(commands=['convert'])
def replying(message):
  bot.send_message(message.chat.id, "Please Send A Word or A PDF Document")
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
    else:
        bot.send_message(message.chat.id, "Please Send PDF or Word Documents Only")
        empty_converted()
        empty_downloaded()
         

bot.infinity_polling()
keep_alive.keep_alive()
