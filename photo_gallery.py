import logging
import os
import pandas as pd
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from googleapi import *
from Google import Create_Service

API_NAME = 'drive'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES) 
print(dir(service))
reply_keyboard = [['Untitled folder','Sitting', 'Sleeping', 'Baby']
				,['Cone','Outside','Hoomans','testing']]
# name_list = pd.read_csv(R"imglinks.csv")
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text("This bot sends you photos of our beloved family pet! Send /photo to start.")
def photo(update, context):
    choice = update.message.reply_text(
        "Choose a category of photos and you'll be sent the photos",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    print("choice",choice) #use replykeyboardmarkup and set one_time_keyboard to true to make it disappear after selection is made
    return choice 
def reply(update, context):
    print('in reply')
    user_input = update.message.text # store user input
    print("user input",user_input)
    # update_name = name_list[name_list['testing']==user_input] # filter matching table by category
    # print("update message",update_name,"ends here")
    # for i in range(0,len(update_name)): # loop to send the photos using the unique identifier + the imgur url header
    dir = os.listdir('/home/actoinfi/presonal datas/telegram bot/photo_uploading_bot/down')
    length = len(dir)
    file_listing(user_input,service,length)
    for i in dir:
        url = open('down/'+i, 'rb')
        print('url',url)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url) 

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    
    updater = Updater("1758192696:AAG4ByVgkFKoeWBvKxrnljd8mTDctgji_Eg", use_context=True)
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('photo',photo))
    dp.add_handler(MessageHandler(Filters.regex('^(Sitting|Sleeping|Baby|Cone|Outside|Hoomans)$'), reply))    
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()