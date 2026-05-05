"""
handlers/exercise.py — /exercise command and inline-button callbacks.

Provides a categorised exercise library with tips for each movement.
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

EXERCISE_CATEGORIES: dict[str, dict] = {
    "chest": {
        "label": "🏋️ Chest",
        "exercises": {
            "Bench Press": (
                "📌 *Bench Press*\n\n"
                "• *Muscles:* Pectorals, Triceps, Anterior Deltoid\n"
                "• *Equipment:* Barbell or Dumbbells\n\n"
                "✅ *Tips:*\n"
                "— Keep shoulder blades pinched together.\n"
                "— Bar should touch mid-chest, not neck.\n"
                "— Drive feet into the floor for leg drive.\n"
                "— Control the descent (2 s down)."
            ),
            "Push-Up": (
                "📌 *Push-Up*\n\n"
                "• *Muscles:* Pectorals, Triceps, Core\n"
                "• *Equipment:* None (bodyweight)\n\n"
                "✅ *Tips:*\n"
                "— Keep body straight — no sagging hips.\n"
                "— Hands slightly wider than shoulder-width.\n"
                "— Look at the floor, not forward.\n"
                "— Full range of motion — chest nearly touches floor."
            ),
        },
    },
    "legs": {
        "label": "🦵 Legs",
        "exercises": {
            "Squat": (
                "📌 *Squat*\n\n"
                "• *Muscles:* Quads, Glutes, Hamstrings, Core\n"
                "• *Equipment:* Barbell / Dumbbells / Bodyweight\n\n"
                "✅ *Tips:*\n"
                "— Feet shoulder-width apart, toes slightly out.\n"
                "— Keep chest up and back neutral.\n"
                "— Knees track over toes — don't cave inward.\n"
                "— Aim to break parallel (thighs below parallel)."
            ),
            "Romanian Deadlift": (
                "📌 *Romanian Deadlift*\n\n"
                "• *Muscles:* Hamstrings, Glutes, Lower Back\n"
                "• *Equipment:* Barbell or Dumbbells\n\n"
                "✅ *Tips:*\n"
                "— Hinge at the hips, not the waist.\n"
                "— Keep the bar close to the legs.\n"
                "— Stop when you feel a stretch in hamstrings.\n"
                "— Maintain a neutral spine throughout."
            ),
        },
    },
    "back": {
        "label": "🔙 Back",
        "exercises": {
            "Pull-Up": (
                "📌 *Pull-Up*\n\n"
                "• *Muscles:* Lats, Biceps, Rear Deltoid\n"
                "• *Equipment:* Pull-up bar\n\n"
                "✅ *Tips:*\n"
                "— Start from a dead hang.\n"
                "— Pull elbows down and back.\n"
                "— Chin clears the bar at the top.\n"
                "— Lower yourself fully — don't half-rep."
            ),
            "Barbell Row": (
                "📌 *Barbell Row*\n\n"
                "• *Muscles:* Lats, Rhomboids, Biceps, Lower Back\n"
                "• *Equipment:* Barbell\n\n"
                "✅ *Tips:*\n"
                "— Hinge torso to ~45° or parallel to floor.\n"
                "— Pull bar to belly button, not chest.\n"
                "— Keep core braced — no rounding.\n"
                "— Squeeze shoulder blades at the top."
            ),
        },
    },
    "core": {
        "label": "🧘 Core",
        "exercises": {
            "Plank": (
                "📌 *Plank*\n\n"
                "• *Muscles:* Transverse Abdominis, Obliques, Glutes\n"
                "• *Equipment:* None (bodyweight)\n\n"
                "✅ *Tips:*\n"
                "— Forearms shoulder-width, elbows under shoulders.\n"
                "— Squeeze glutes and abs simultaneously.\n"
                "— Keep hips level — no piking or sagging.\n"
                "— Breathe steadily; don't hold your breath."
            ),
            "Bicycle Crunch": (
                "📌 *Bicycle Crunch*\n\n"
                "• *Muscles:* Rectus Abdominis, Obliques\n"
                "• *Equipment:* None (bodyweight)\n\n"
                "✅ *Tips:*\n"
                "— Hands loosely behind head — don't pull neck.\n"
                "— Rotate torso, not just elbow.\n"
                "— Extend the non-working leg low to the floor.\n"
                "— Move in a slow, controlled rhythm."
            ),
        },
    },
}


def _category_keyboard() -> InlineKeyboardMarkup:
    """Build inline keyboard showing all exercise categories."""
    buttons = [
        [InlineKeyboardButton(data["label"], callback_data=f"exercise_cat_{key}")]
        for key, data in EXERCISE_CATEGORIES.items()
    ]
    return InlineKeyboardMarkup(buttons)


def _exercise_keyboard(category_key: str) -> InlineKeyboardMarkup:
    """Build inline keyboard showing exercises within a category."""
    exercises = EXERCISE_CATEGORIES[category_key]["exercises"]
    buttons = [
        [
            InlineKeyboardButton(
                name, callback_data=f"exercise_detail_{category_key}_{name}"
            )
        ]
        for name in exercises
    ]
    buttons.append(
        [InlineKeyboardButton("⬅️ Back to categories", callback_data="exercise_back")]
    )
    return InlineKeyboardMarkup(buttons)


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def exercise_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show exercise categories."""
    await update.message.reply_text(
        "📚 *Exercise Library*\nChoose a muscle group:",
        parse_mode="Markdown",
        reply_markup=_category_keyboard(),
    )


async def exercise_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle category selection and individual exercise detail."""
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == "exercise_back":
            await query.edit_message_text(
                "📚 *Exercise Library*\nChoose a muscle group:",
                parse_mode="Markdown",
                reply_markup=_category_keyboard(),
            )

        elif data.startswith("exercise_cat_"):
            category_key = data.replace("exercise_cat_", "")
            category = EXERCISE_CATEGORIES.get(category_key)
            if category is None:
                await query.edit_message_text("❌ Category not found.")
                return
            await query.edit_message_text(
                f"{category['label']} — choose an exercise:",
                reply_markup=_exercise_keyboard(category_key),
            )

        elif data.startswith("exercise_detail_"):
            # Format: exercise_detail_{category}_{exercise name}
            parts = data.replace("exercise_detail_", "").split("_", 1)
            if len(parts) != 2:
                await query.edit_message_text("❌ Invalid selection.")
                return
            category_key, exercise_name = parts
            category = EXERCISE_CATEGORIES.get(category_key)
            if category is None or exercise_name not in category["exercises"]:
                await query.edit_message_text("❌ Exercise not found.")
                return
            detail = category["exercises"][exercise_name]
            back_button = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅️ Back",
                            callback_data=f"exercise_cat_{category_key}",
                        )
                    ]
                ]
            )
            await query.edit_message_text(
                detail, parse_mode="Markdown", reply_markup=back_button
            )

    except Exception as exc:
        logger.error("exercise_callback_handler error: %s", exc)
        await query.edit_message_text(
            "⚠️ Something went wrong. Please try /exercise again."
        )
