from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,MessageEntity
import requests
import re
import logging
import os
import sys

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
GROUP_ID= os.getenv("GROUP_ID")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)
def get_random_dog_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def bop(bot, update):
    #sends cool random dog pictures
    url = get_random_dog_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

FLAG_OFFSET= 127462 - ord('A')         
def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + FLAG_OFFSET) + chr(ord(code[1]) + FLAG_OFFSET)
def startBot(bot,update):
    msg="Hey, Good to meet you.\nWelcome To SOLOLEARN NIGERIA"+flag("ng")+ " Telegram Bot.\nDesigned and maintained by SOLOLEARN NIGERIA"+flag("ng")+" group members.\nEnter the /help command to see available helps."
    update.message.reply_text(msg)
def showHelp(bot,update):
    msg="Currently, No help is available"
    update.message.reply_text(msg)
if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('help',showHelp))
    dp.add_handler(CommandHandler('start',startBot))
    run(updater)
