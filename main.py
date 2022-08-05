#!/usr/bin/env python
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from yelp import search_yelp, find_hours

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import imdb
import recipes
import finishline
import translator
import movie_quote

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#----------- Lindsey's code ---------
STORE = range(1)
storage = []


def search(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reply_keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']]
    try:
        find = context.args[0]
        city = context.args[1]
        state = context.args[2]
        if context.args[3]:
            zip = context.args[3]
        else:
            zip = None
    except (IndexError, ValueError):
        update.message.reply_text('Syntaxt Error. Usage: /search <text to search> <city> <state> <Optional: zip>')
    options = search_yelp(find, city, state, zip)
    stores = options[0]
    storage.append(stores)
    storage.append(options[1])
    for i in range(0, len(stores)):
        update.message.reply_text("[%d] %s" % (i+1, stores[i]))
    update.message.reply_text("Here are the top 10 Yelp results for your search. Type the number corresponding to the business you want to see the hours of",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return STORE

def store(update: Update, context: CallbackContext):
    user = update.message.from_user
    selection = update.message.text
    print(selection)
    hours = find_hours(storage[0], storage[1], selection)
    update.message.reply_text("The hours for this business are: %s" % hours)

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Search cancelled. Thanks, see you later!")
    return ConversationHandler.END

#------------------------------------

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def movie(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    result = imdb.lookup(" ".join(context.args))
    update.message.reply_text(
        result
    )

def recipe(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    result = recipes.recipe(" ".join(context.args))
    update.message.reply_text(
        result
    )

def shoes(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    result = finishline.finishline()
    update.message.reply_text(
        result
    )

def yelp(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    result = "" #TODO
    update.message.reply_text(
        result
    )

def translate(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    result = translator.translate(" ".join(context.args))
    update.message.reply_text(
        result
    )

def quote(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    result = movie_quote.moviequote()
    update.message.reply_text(
        result
    )

def main() -> None:
    """Start the bot."""
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('search', search)],
        states={
            STORE: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|10)$'), store)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("yelp", search))

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("movie", movie))
    dispatcher.add_handler(CommandHandler("recipe", recipe))
    dispatcher.add_handler(CommandHandler("shoes", shoes))
    dispatcher.add_handler(CommandHandler("yelp", yelp))
    dispatcher.add_handler(CommandHandler("translate", translate))
    dispatcher.add_handler(CommandHandler("quote", quote))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
