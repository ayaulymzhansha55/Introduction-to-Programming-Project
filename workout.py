"""
handlers/workout.py — /workout command and inline-button callbacks.

Provides three pre-built workout plans selectable via inline keyboard.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

WORKOUT_PLANS: dict[str, dict] = {
    "beginner": {
        "title": "🟢 Beginner Full-Body (3×/week)",
        "description": (
            "A simple 3-day-per-week plan to build a solid foundation.\n\n"
            "*Day A — Push*\n"
            "• Bodyweight Squats — 3×12\n"
            "• Push-Ups — 3×10\n"
            "• Dumbbell Shoulder Press — 3×10\n"
            "• Plank — 3×30 s\n\n"
            "*Day B — Pull*\n"
            "• Dumbbell Rows — 3×10\n"
            "• Lat Pull-Down — 3×10\n"
            "• Bicep Curls — 3×12\n"
            "• Dead Bug — 3×10\n\n"
            "*Day C — Legs*\n"
            "• Goblet Squats — 3×12\n"
            "• Romanian Deadlift — 3×10\n"
            "• Glute Bridge — 3×15\n"
            "• Calf Raises — 3×15\n\n"
            "Rest 60–90 s between sets."
        ),
    },
    "intermediate": {
        "title": "🟡 Intermediate Push/Pull/Legs (5×/week)",
        "description": (
            "A classic PPL split for intermediate lifters.\n\n"
            "*Push Day*\n"
            "• Bench Press — 4×8\n"
            "• Overhead Press — 3×8\n"
            "• Incline Dumbbell Press — 3×10\n"
            "• Tricep Dips — 3×12\n\n"
            "*Pull Day*\n"
            "• Barbell Row — 4×8\n"
            "• Pull-Ups — 3×8\n"
            "• Face Pulls — 3×15\n"
            "• Hammer Curls — 3×12\n\n"
            "*Leg Day*\n"
            "• Squat — 4×6\n"
            "• Romanian Deadlift — 3×10\n"
            "• Leg Press — 3×12\n"
            "• Walking Lunges — 3×12\n\n"
            "Rest 2–3 min on compound lifts."
        ),
    },
    "cardio": {
        "title": "🔵 Cardio & HIIT Plan (4×/week)",
        "description": (
            "Burn fat and improve endurance with mixed cardio.\n\n"
            "*Day 1 — Steady State*\n"
            "• 30–45 min jog at 60–70% max HR\n\n"
            "*Day 2 — HIIT*\n"
            "• Warm-up: 5 min light jog\n"
            "• 8 rounds: 30 s sprint → 90 s walk\n"
            "• Cool-down: 5 min walk\n\n"
            "*Day 3 — Cross Training*\n"
            "• Cycling, swimming, or rowing — 30 min\n\n"
            "*Day 4 — HIIT + Core*\n"
            "• 6 rounds: 40 s Burpees → 20 s rest\n"
            "• Plank 3×45 s\n"
            "• Mountain Climbers 3×20\n"
        ),
    },
}


def _build_plan_keyboard() -> InlineKeyboardMarkup:
    """Return inline keyboard with one button per workout plan."""
    buttons = [
        [InlineKeyboardButton(data["title"], callback_data=f"workout_{key}")]
        for key, data in WORKOUT_PLANS.items()
    ]
    return InlineKeyboardMarkup(buttons)


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def workout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available workout plans as inline buttons."""
    await update.message.reply_text(
        "🏋️ *Choose a Workout Plan:*",
        parse_mode="Markdown",
        reply_markup=_build_plan_keyboard(),
    )


async def workout_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send the selected workout plan details."""
    query = update.callback_query
    await query.answer()

    plan_key = query.data.replace("workout_", "")
    plan = WORKOUT_PLANS.get(plan_key)

    if plan is None:
        logger.warning("Unknown workout plan key: %s", plan_key)
        await query.edit_message_text("❌ Plan not found. Please try again.")
        return

    await query.edit_message_text(
        f"*{plan['title']}*\n\n{plan['description']}",
        parse_mode="Markdown",
    )
