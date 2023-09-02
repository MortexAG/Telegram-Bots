import os
import telebot
import convertapi
import glob
import keep_alive
import datetime
from datetime import datetime
import PIL
from PIL import Image
import sqlite3


#os.system("python3 -m poetry remove telebot")
BOT_API = os.environ["BOT_API"]
API_SECRET = os.environ['API_SECRET']
owner = os.environ['owner']

# Path Checks For The Important Directories

if os.path.exists("./converted"):
  pass
else:
  os.mkdir("./downloaded")
  
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

conn = sqlite3.connect('conversion_data.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS conversion_count (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  count INTEGER)''')

# Initialize the count to 0 if no count exists 
cursor.execute('SELECT count FROM conversion_count')
result = cursor.fetchone()
if result is None:
    initial_count = 0
    cursor.execute('INSERT INTO conversion_count (count) VALUES (?)', (initial_count,))
else:
    initial_count = result[0]

# Commit the changes and close the connection
conn.commit()
conn.close()


# Add To The Count 
count_data = {'count': initial_count}

def increment_count():
    count_data['count'] += 1
    print(count_data['count'])
    conn = sqlite3.connect('conversion_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE conversion_count SET count = ?', (count_data['count'],))
    conn.commit()
    conn.close()
    return count_data['count']
# Function to reset the count to zero
def reset_count():
    count_data['count'] = 0
    cursor.execute('UPDATE conversion_count SET count = ?', (count_data['count'],))
    conn.commit()
    conn.close()
    return count_data['count']



bot = telebot.TeleBot(BOT_API)
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


def get_current_time():
  times = datetime.now()
  now = times.strftime("%Y-%m-%d, %H:%M:%S")
  return now

def word_to_pdf():
  convertapi.api_secret = API_SECRET
  convertapi.convert('pdf', {
    'File': "./downloaded/"+file_name
}, from_format = 'docx').save_files('./converted')
  #increment_count()
  
def pdf_to_word():
  convertapi.api_secret = API_SECRET
  convertapi.convert('word', {
    'File': "./downloaded/"+file_name
}, from_format = 'pdf').save_files('./converted')
  #increment_count()

def ppt_to_pdf():
  convertapi.api_secret = API_SECRET
  convertapi.convert('pdf', {
    'File': "./downloaded/"+file_name
}, from_format = 'ppt').save_files('./converted')
  #increment_count()
def pptx_to_pdf():
  convertapi.api_secret = API_SECRET
  convertapi.convert('pdf', {
    'File': "./downloaded/"+file_name
}, from_format = 'pptx').save_files('./converted')
  #increment_count()

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

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Send A Word Or A PDF Or A Powerpoint Document or An Image Directly in This Chat To Convert It")

@bot.message_handler(commands=['reset'])
def reset_conversion_count(message):
  if int(message.from_user.id) == int(owner):
    bot.send_message(message.chat.id,"Conversions Count Is Now Reset To Zero")
    reset_count()
  else:
    bot.send_message(message.from_user.id, "Sorry Only The Owner Can Use This Command")

@bot.message_handler(commands=['count'])
def current_count(message):
  if int(message.from_user.id) == int(owner):
    conn_current = sqlite3.connect('conversion_data.db')
    cursor_current = conn_current.cursor()
    cursor_current.execute('SELECT count FROM conversion_count')
    current_count = cursor_current.fetchone()
    bot.send_message(message.chat.id, f"Current Count Is {current_count}")
    conn_current.commit()
    conn_current.close()
  else:
    bot.send_message(message.from_user.id, "Sorry Only The Owner Can Use This Command")

#@bot.message_handler(commands=['add'])
#def add_one(message):
#  if int(message.from_user.id) == int(owner):
#    current_count = increment_count()
#    bot.send_message(message.chat.id, f"Conversions Count Increased By One And Now Is {current_count}")
#  else:
#    bot.send_message(message.from_user.id, "Sorry Only The Owner Can Use This Command")

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
    global the_filename 
    the_filename = file_name
    file_type = message.document.mime_type
    with open("./downloaded/"+file_downloaded, 'wb') as new_file:
        new_file.write(downloaded_file)

        # check of the bot uses ran out
    if  initial_count >= 250 or initial_count == 249:
      bot.send_message(owner, "The Bot Count Reached 250 Please Renew The API Token")
      bot.send_message(message.chat.id, "Sorry The Bot Is Offline Now Pleasae Come Back Later")
      bot.send_message(message.chat.id,"Your Documemt Was Deleted And Was Not Saved By The Bot")

      # check if it's a word document

    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      bot.reply_to(message, "Word Document Recieved, Please Wait")
      try:
        word_to_pdf()
        bot.send_message(message.chat.id, "Word Converted To PDF")
        for filename in glob.glob('converted/*'):
          pdf_converted = open(filename, "rb")
          bot.send_document(message.chat.id, pdf_converted)
          increment_count()
      except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "There Was An Error Converting The File Try Again or Try Later")
        empty_converted()
        empty_downloaded()

      # check if it's a pdf
    
    elif file_type == "application/pdf":
      bot.reply_to(message, "PDF Document Recieved, Please Wait")
      try:
        pdf_to_word()
        bot.send_message(message.chat.id, "PDF Converted To Word")
        for filename in glob.glob('converted/*'):
          word_converted = open(filename, "rb")
          bot.send_document(message.chat.id, word_converted)
          increment_count()
      except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "There Was An Error Converting The File Try Again or Try Later")
      empty_converted()
      empty_downloaded()
    
        # check if it's a ppt or pptx

    elif file_type in("application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.ms-powerpoint"):
        bot.reply_to(message, "Powerpoint Document Recieved, Please Wait")
        try:
          powerpoint_to_pdf()
          for filename in glob.glob('converted/*'):
            powerpoint_converted = open(filename, 'rb')
            bot.send_message(message.chat.id, "Powerpoint Converted To PDF")
            bot.send_document(message.chat.id, powerpoint_converted)
            increment_count()
        except Exception as e:
          print(e)
          bot.send_message(message.chat.id, "There Was An Error Converting The File Try Again or Try Later")    
        empty_converted()
        empty_downloaded()
                
    else:
        print(file_type)
        bot.send_message(message.chat.id, file_type)
        bot.send_message(message.chat.id, "Please Send PDF or Word Documents Only")
        empty_converted()
        empty_downloaded()
@bot.message_handler(commands=['about', 'source'])
def about(message):
    bot.send_message(message.chat.id, "This Bot Was Created By @AhmedGouda100")
    bot.send_message(message.chat.id, "I Was Created With Python And My Source Code is Here https://github.com/MortexAG/Telegram-Bots/tree/main/Document-Converter")


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
