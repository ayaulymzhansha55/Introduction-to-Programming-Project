"""
handlers/start.py — /start command handler.
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["/workout", "/exercise"],
        ["/log", "/progress"],
    ],
    resize_keyboard=True,
)

WELCOME_TEXT = (
    "💪 *Welcome to FitBot!*\n\n"
    "Here's what I can do for you:\n\n"
    "🏋️ /workout — Browse workout plans\n"
    "📚 /exercise — Explore exercise library\n"
    "📝 /log — Log a workout session\n"
    "📊 /progress — View your progress history\n\n"
    "Pick an option from the menu below to get started!"
)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message and show the main menu."""
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=MAIN_MENU,
    )
