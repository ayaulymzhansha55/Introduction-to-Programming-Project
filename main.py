"""
Fitness Telegram Bot - Main Entry Point
"""

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

from handlers.start import start_handler
from handlers.workout import (
    workout_handler,
    workout_callback_handler,
)
from handlers.progress import (
    log_progress_handler,
    view_progress_handler,
)
from handlers.exercise import exercise_handler, exercise_callback_handler
from config import BOT_TOKEN

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("workout", workout_handler))
    app.add_handler(CommandHandler("exercise", exercise_handler))
    app.add_handler(CommandHandler("log", log_progress_handler))
    app.add_handler(CommandHandler("progress", view_progress_handler))

    # Callback query handlers (inline buttons)
    app.add_handler(CallbackQueryHandler(workout_callback_handler, pattern="^workout_"))
    app.add_handler(CallbackQueryHandler(exercise_callback_handler, pattern="^exercise_"))

    logger.info("Bot started successfully.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
