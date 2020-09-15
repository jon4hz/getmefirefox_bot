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
    return ReplyKeyboardMarkup([[KeyboardButton(button_command['image']), KeyboardButton(button_command['video'])]],
            resize_keyboard=True,
            one_time_keyboard=False)


def message_handler_buttons(update, context):
    if update.message.text == button_command['image']:
        bopimage(update, context)
    elif update.message.text == button_command['video']:
        bopvideo(update, context)


#==================================================================================================
# BOT FUNCTIONS
#==================================================================================================

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the Doggo Bot. Use /bopimage to get doggo images and use /bopvideo to get doggo videos. Enjoy!', reply_markup=reply_keyboard_markup())


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Use /bopimage to get a doggo image and /bopvideo to get a doggo video')


def bopvideo(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
    url = get_video_url()
    context.bot.send_video(chat_id=update.effective_chat.id, video=url)


def bopimage(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    url = get_image_url()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


# Inline Query handler
def InlineBopVideo(update, context):
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id = uuid4(),
            title = "bopvideo",
            input_message_content = InputMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode = ParseMode.MARKDOWN
            )
        )
    ]

    update.inline_query.answer(results)


#==================================================================================================
# MAIN
#==================================================================================================

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('bopimage',bopimage))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('bopvideo',bopvideo))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(MessageHandler(Filters.text, message_handler_buttons))
    dp.add_error_handler(InlineQueryHandler(InlineBopVideo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

