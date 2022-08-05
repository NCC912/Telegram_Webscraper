'''
Here's the bot I made (minus the API token). I wanted to upload it cause there's a couple things like Conversation
Handlers I had to implement to make it work, so I wanted to make sure we all had access to this for the final bot.

This bot (using functions in the yelp.py file) allows the user to search for an item or business on Yelp, displays the top 10
results, allows the user to choose a business from those results, and then displays that business' hours. 

Note that right now, the code only works if all your arguments are 1 word
(it won't give you accurate results if you search for "ice cream" or say your city is "Las Vegas", for example)
Working on getting this fixed, sorry for any inconvenience
'''

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from yelp import search_yelp, find_hours
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
storage = []

STORE = range(1)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Yelp bot. Type /help for command options")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("To do a Yelp search, type /search <text to search> <city> <state> <zip code>"
    "You will then be given the top 10 search results, and after choosing one, I will tell you the hours of that business."
    "Make sure for state you type the state's acronym (e.g. for California you'd type CA")

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


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("API Token would go here")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('search', search)],
        states={
            STORE: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|10)$'), store)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("search", search))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__=='__main__':
    main()
