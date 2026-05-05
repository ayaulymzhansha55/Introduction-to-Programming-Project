"""
handlers/progress.py — /log and /progress command handlers.

/log  <exercise> <sets> <reps> [weight_kg] [notes]
    Example: /log "Bench Press" 3 10 80 "felt strong today"

/progress — displays the user's last 10 logged sessions.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from database import insert_log, fetch_logs

logger = logging.getLogger(__name__)

LOG_USAGE = (
    "📝 *How to log a workout:*\n\n"
    "`/log <exercise> <sets> <reps> [weight_kg] [notes]`\n\n"
    "*Examples:*\n"
    "`/log Squat 4 8 100`\n"
    "`/log Plank 3 60 0 felt strong today`\n\n"
    "• weight\\_kg is optional (default 0)\n"
    "• notes are optional"
)


def _parse_log_args(args: list[str]) -> tuple[str, int, int, float, str]:
    """
    Parse command arguments into (exercise, sets, reps, weight_kg, notes).
    Raises ValueError with a human-friendly message on bad input.
    """
    if len(args) < 3:
        raise ValueError("Not enough arguments.")

    exercise = args[0]
    try:
        sets = int(args[1])
        reps = int(args[2])
    except ValueError:
        raise ValueError("Sets and reps must be whole numbers (e.g. 3 10).")

    if sets <= 0 or reps <= 0:
        raise ValueError("Sets and reps must be positive numbers.")

    weight_kg = 0.0
    notes = ""

    if len(args) >= 4:
        try:
            weight_kg = float(args[3])
        except ValueError:
            raise ValueError("Weight must be a number (e.g. 80 or 0).")

    if len(args) >= 5:
        notes = " ".join(args[4:])

    return exercise, sets, reps, weight_kg, notes


async def log_progress_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handle /log command — parse arguments and save to DB.
    Usage: /log <exercise> <sets> <reps> [weight_kg] [notes]
    """
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text(LOG_USAGE, parse_mode="Markdown")
        return

    try:
        exercise, sets, reps, weight_kg, notes = _parse_log_args(args)
    except ValueError as exc:
        await update.message.reply_text(
            f"⚠️ {exc}\n\n{LOG_USAGE}",
            parse_mode="Markdown",
        )
        return

    try:
        insert_log(user_id, exercise, sets, reps, weight_kg, notes)
    except Exception as exc:
        logger.error("DB error for user %s: %s", user_id, exc)
        await update.message.reply_text(
            "❌ Could not save your log. Please try again later."
        )
        return

    weight_str = f" @ {weight_kg} kg" if weight_kg else ""
    notes_str = f"\n📝 _{notes}_" if notes else ""
    await update.message.reply_text(
        f"✅ *Logged!*\n\n"
        f"🏋️ {exercise} — {sets}×{reps}{weight_str}{notes_str}",
        parse_mode="Markdown",
    )


async def view_progress_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle /progress command — show the user's last 10 workout logs."""
    user_id = update.effective_user.id

    try:
        rows = fetch_logs(user_id, limit=10)
    except Exception as exc:
        logger.error("DB fetch error for user %s: %s", user_id, exc)
        await update.message.reply_text(
            "❌ Could not retrieve your progress. Please try again later."
        )
        return

    if not rows:
        await update.message.reply_text(
            "📊 No logs yet! Use /log to record your first workout."
        )
        return

    lines = ["📊 *Your Last 10 Workouts:*\n"]
    for row in rows:
        weight_str = f" @ {row['weight_kg']} kg" if row["weight_kg"] else ""
        notes_str = f" — _{row['notes']}_" if row["notes"] else ""
        lines.append(
            f"• `{row['date']}` — *{row['exercise']}* "
            f"{row['sets']}×{row['reps']}{weight_str}{notes_str}"
        )

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
