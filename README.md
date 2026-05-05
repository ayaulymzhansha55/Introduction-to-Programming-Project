# Introduction-to-Programming-Project
telegram bot
"""
bot.py — FitBot entry point.

Run
---
    pip install -r requirements.txt
    BOT_TOKEN=<your_token> python bot.py

Environment
-----------
BOT_TOKEN : str("8660406856:AAEFF28EQxjkDU_Nd8WbRr806_YMgC9k5UE")
LOG_LEVEL : str  (optional) Python log level, default INFO
"""

from __future__ import annotations

import logging
import os
from datetime import time as dtime

from telegram.ext import Application

import database as db
from handlers import register_handlers, send_daily_reminder

# ─── Logging setup ────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
)
logger = logging.getLogger(__name__)


# ─── Scheduler helper ─────────────────────────────────────────────────────────

def _schedule_reminders(app: Application) -> None:
    """
    Load all saved reminders from the DB and register them with the job queue.

    Each reminder is a daily job firing at the user's chosen UTC time.
    """
    reminders = db.get_all_reminders()
    for row in reminders:
        user_id = row["user_id"]
        h, m = map(int, row["time_utc"].split(":"))
        app.job_queue.run_daily(
            callback=send_daily_reminder,
            time=dtime(h, m),
            data=user_id,
            name=f"reminder_{user_id}",
        )
    logger.info("Scheduled %d reminder(s)", len(reminders))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Initialise the bot and start polling."""
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise EnvironmentError(
            "BOT_TOKEN environment variable is not set. "
            "Get a token from @BotFather on Telegram."
        )

    # Initialise database
    db.init_db()

    # Build the application
    app = (
        Application.builder()
        .token(token)
        .build()
    )

    # Attach all command / conversation handlers
    register_handlers(app)

    # Schedule persisted reminders
    _schedule_reminders(app)

    logger.info("FitBot is running — press Ctrl-C to stop")
     app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

