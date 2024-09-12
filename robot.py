#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram Bot that replies to messages and includes a button for launching a mini-app.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting message and a button to launch the mini app."""
    user = update.effective_user

    # Create a button to launch the Web App (mini app)
    button = InlineKeyboardButton(text="Open Mini App", web_app={"url": "https://naatic.esube.com.et/mini-app"})
    keyboard = InlineKeyboardMarkup([[button]])

    # Send a greeting message with the button
    await update.message.reply_html(
        text=f"Hi {user.mention_html()}! Click the button below to launch the mini app.",
        reply_markup=keyboard,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("This bot can help you interact with the NAATIC mini-app. Use /start to begin!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Load environment variables
    load_dotenv()

    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.environ["TOKEN"]).build()

    # Handlers for commands like /start and /help
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Echo handler for non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot and run until manually stopped (Ctrl + C)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
