import telebot
import os
import dotenv
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
from email.mime.text import MIMEText
import time
load_dotenv()

# Initialize the Telegram bot
BOT_API = os.environ['BOT_API']
bot = telebot.TeleBot(BOT_API)
myid = os.environ['myid']

# Initialize the Gmail API credentials
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', ['https://www.googleapis.com/auth/gmail.readonly'])
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Initialize the Gmail API client
service = build('gmail', 'v1', credentials=creds)

# Define a function to get the latest email and send it to the chat
def send_latest_email(chat_id):
    try:
        # Get the latest email from the user's inbox
        result = service.users().messages().list(userId='me', maxResults=1).execute()
        message = result.get('messages', [])
        if message:
            msg = service.users().messages().get(userId='me', id=message[0]['id'], format='full').execute()
            sender = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'][0]
            subject = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'][0]
            body = msg['snippet']
            message_text = f"From: {sender}\nSubject: {subject}\n\n{body}"
            
            # Check if the message has an attachment
            bot.send_message(chat_id, message_text)
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    # Check if the part is an attachment
                    if part.get('filename') and part.get('body') and part.get('body').get('attachmentId'):
                        attachment = service.users().messages().attachments().get(userId='me', messageId=msg['id'], id=part['body']['attachmentId']).execute()
                        attachment_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                        
                        # Create the attachments directory if it doesn't exist
                        if not os.path.exists('attachments'):
                            os.makedirs('attachments')
                            
                        # Save the attachment to a file
                        file_name = f"attachments/{part['filename']}"
                        with open(file_name, 'wb') as f:
                            f.write(attachment_data)
                            
                        # Send the file to the chat
                        with open(file_name, 'rb') as f:
                            bot.send_document(chat_id, f)
                            
                        # Delete the file
                        os.remove(file_name)
                        
                        # Add a message to the message_text indicating that an attachment was sent
                        #message_text += "\n\nAttachment sent."
                        
            # Send the message text to the chat
    except HttpError as error:
        print(f"An error occurred: {error}")




# Define a handler for the "/start" command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(myid, "Hello! I will send you any new email in your inbox.")

# Define a handler to send the latest email on demand
@bot.message_handler(commands=['latest_email'])
def latest_email(message):
    send_latest_email(myid)

# Define a function to check for new emails periodically
def check_new_emails():
    chat_id = myid
    latest_email_id_stored = None

    while True:
        try:
            # Check if there are any new emails
            service = build('gmail', 'v1', credentials=creds)
            result = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
            messages = result.get('messages', [])

            if messages:
                # Get the ID of the latest email
                latest_email = messages[-1]
                latest_email_id = latest_email['id']

                # Check if the latest email is newer than the stored ID
                if not latest_email_id == latest_email_id_stored:
                    # Send the new email to the chat
                    send_latest_email(chat_id)

                    # Update the stored latest email ID
                    latest_email_id_stored = latest_email_id
        except Exception as e:
            print(e)

        # Wait for 60 seconds before checking for new emails again
        time.sleep(5)


# Start the bot and check for new emails
if __name__ == '__main__':
    check_new_emails()
