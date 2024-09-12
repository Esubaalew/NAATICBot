from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import logging
from dotenv import load_dotenv
import os
import asyncio

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting message and a button to launch the mini app."""
    chat_id = update.effective_chat.id

    # Create a button to launch the Web App
    button = InlineKeyboardButton(text="Open Mini App", web_app={"url": "https://naatic.esube.com.et/mini-app"})
    keyboard = InlineKeyboardMarkup([[button]])

    # Send a greeting message with the button
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Hello! {update.effective_chat.first_name}, I am NAATICbot. I am here to help you with your NAATIC experience. Click the button below to launch the mini app.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

async def main() -> None:
    """Start the bot."""
    # Load environment variables
    load_dotenv()
    application = Application.builder().token(os.environ['TOKEN']).build()

    # Add command handler for the `/start` command
    application.add_handler(CommandHandler("start", start))

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    try:
        # Check if there is already an event loop running
        loop = asyncio.get_running_loop()
    except RuntimeError:  # If no event loop is running, create one
        loop = None

    if loop and loop.is_running():
        logger.info("Detected running event loop. Scheduling main() on the existing loop.")
        # Schedule main() coroutine on the existing loop
        asyncio.ensure_future(main())
    else:
        logger.info("No running event loop detected. Starting a new one.")
        # Start a new event loop
        asyncio.run(main())
