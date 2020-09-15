#!/usr/bin/env pytho
#
# Author:   jonah
# Date:     14.11.2019
# Desc:     Telegram BOT, which sends a random dog image or video
#
###################################################################################################
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters 
from telegram import KeyboardButton, ReplyKeyboardMarkup, ChatAction, InlineQueryResultArticle, ParseMode, InputMessageContent
from telegram.utils.helpers import escape_markdown
import requests
import re

#==================================================================================================
# VARIABLES
#==================================================================================================

with open('token.txt') as f:
    TOKEN = f.read()

emoji = {'image':'\U0001F4F7'}
button_command = {'image': f'{emoji["image"]} Image'}


troll = [1043623788]

#==================================================================================================
# FUNCTIONS
#==================================================================================================

def get_url():
    contents = requests.get('https://some-random-api.ml/img/red_panda').json()
    url = contents['link']
    return url


def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def get_video_url():
    allowed_extension = ['mp4', 'gif']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def reply_keyboard_markup():
    return ReplyKeyboardMarkup([[KeyboardButton(button_command['image'])]],
            resize_keyboard=True,
            one_time_keyboard=False)


def message_handler_buttons(update, context):
    if update.message.text == button_command['image']:
        bopimage(update, context)
    

#==================================================================================================
# BOT FUNCTIONS
#==================================================================================================

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the red panda Bot. Use /bopimage to get red panda images. Enjoy!', reply_markup=reply_keyboard_markup())


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Use /bopimage to get a red panda image.')


def bopimage(update, context):
    if update.message.chat.id in troll:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_video(chat_id=update.effective_chat.id, video=open('RickRoll.mp4', 'rb'))
    else:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        url = get_image_url()
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


#==================================================================================================
# MAIN
#==================================================================================================

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('bopimage',bopimage))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(MessageHandler(Filters.text, message_handler_buttons))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()