import os
import telebot
import glob
import time
import yt_dlp
from yt_dlp import YoutubeDL
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

def get_quality():
  file_size = "./downloaded/{}.mp4".format(video_title)
  file_stats = os.stat(file_size)
  true_size = (file_stats.st_size / (1024 * 1024))
  print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')
@bot.message_handler(commands=["start", "keyboard"])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Send The Youtube Link Directly In The Chat Then Wait For The Audio To Be Sent")


@bot.message_handler(commands=['empty'])
def replying(message):
  bot.send_message(message.chat.id, "The Bot Storage Is Now Empty")
  empty_converted()
  empty_downloaded()
@bot.message_handler(content_types=['text'])
def link(message):
  with YoutubeDL() as ydl:
    info_dict = ydl.extract_info('{}'.format(message.text), download=False)
    video_url = info_dict.get("url", None)
    video_id = info_dict.get("id", None)
    global video_title
    video_title = info_dict.get('title', None)
    print (video_title)
  yt_dlp_video = "yt-dlp -f 137+140 -o './downloaded/{}.mp4'".format(video_title)
  yt_dlp_low_video = "yt-dlp -f 135+140 -o './downloaded/{}.mp4'".format(video_title)
  yt_dlp_very_low_video = "yt-dlp -f 134+140 -o './downloaded/{}.mp4'".format(video_title)
  yt_dlp_audio = "yt-dlp -o './converted/downloaded.mp3'".format(video_title)
  audio_on = "--extract-audio --audio-format mp3"
  link = message.text
  global audios
  audios = "y"

  if audios == "y":
    bot.send_message(message.chat.id, "The Bot Is Working on It")
    os.system("{} {} {}".format(yt_dlp_audio, audio_on, link))
    time.sleep(1)
    try:
      os.rename("./converted/downloaded.mp3", "./converted/{}.mp3".format(video_title))
      audio = open("./converted/{}.mp3".format(video_title), 'rb')
      bot.send_audio(message.chat.id, audio)
      empty_converted()
      empty_downloaded()
    except:
      audio = open("./converted/downloaded.mp3".format(video_title), 'rb')
      bot.send_message(message.chat.id, video_title)
      bot.send_audio(message.chat.id, audio)
      empty_converted()
      empty_downloaded()
## Below this is a code for downloading videos but was scraped due to limitation on video sending size in telegram but overall it's working well
    def video_downlaod():
      bot.send_message(message.chat.id, "The Bot Is Working on It")
      os.system("{} {}".format(yt_dlp_video, link))
      video = open("./downloaded/{}.mp4".format(video_title), 'rb')
      file_size = "./downloaded/{}.mp4".format(video_title)
      file_stats = os.stat(file_size)
      true_size = (file_stats.st_size / (1024 * 1024))
      print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')
      file_integer = round(true_size)
      if int(file_integer) < 20:
        bot.send_document(message.chat.id, video)
        empty_converted()
        empty_downloaded()
      else:  
        os.system("{} {}".format(yt_dlp_low_video, link))
        get_quality()
        file_stats = os.stat(file_size)
        true_size = (file_stats.st_size / (1024 * 1024))
        file_integer_new = round(true_size)
        if int(file_integer_new) < 55:
          bot.send_message(message.chat.id, "Sorry The Higher Quality is Larger in Size So I Had To Get The 480p Version")
          empty_converted()
          empty_downloaded()
          os.system("{} {}".format(yt_dlp_low_video, link))
          get_quality()
          file_stats = os.stat(file_size)
          true_size = (file_stats.st_size / (1024 * 1024))
          file_integer = round(true_size)
          video_download()
        else:
          bot.send_message(message.chat.id, "Video is Very Large to Be sent")
          empty_converted()
          empty_downloaded()
      
  #video_download
         

bot.infinity_polling()
