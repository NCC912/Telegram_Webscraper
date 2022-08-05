#!/usr/bin/env python

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import imdb
import recipes
import finishline
import translate
import movie_quote

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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
    result = recipe.recipe(" ".join(context.args))
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
    result = translate.translate(" ".join(context.args))
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
