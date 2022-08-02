# THIS FILE IS NOT MEANT TO BE RUN IT'S FOR SAVING SOME NOTES ONLY #



# Red Lines Because Bot is not defined Here

# to allow send location message that can be read
@bot.message_handler(func=lambda message: True,       content_types='location')
     #to allow send a text message that can be read
@bot.message_handler(func=lambda message: True,       content_types='text')
def long(message):
  message = message
  extracted_text = message.text
  
  bot.send_message(message.chat.id, "The message full info")
     #sends the whole message information to the chat
  bot.send_message(message.chat.id, message)
     #extract the text sent in the message
    
