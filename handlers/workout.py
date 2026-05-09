"""
handlers/workout.py — Workout Plans feature.
Offers Beginner / Intermediate / Advanced weekly plans.
"""
 
from telebot import types
 
 
PLANS = {
    "beginner": {
        "title": "🟢 Beginner Plan (3 days/week)",
        "days": [
            ("Monday", "Full-body: 3×10 squats, 3×8 push-ups, 3×10 lunges, 2-min plank"),
            ("Wednesday", "Cardio: 20-min brisk walk + 3×15 glute bridges"),
            ("Friday", "Full-body: 3×10 dumbbell rows, 3×10 shoulder press, 3×12 crunches"),
        ],
    },
    "intermediate": {
        "title": "🟡 Intermediate Plan (4 days/week)",
        "days": [
            ("Monday", "Upper: Bench press 4×8, Rows 4×8, OHP 3×10, Tricep dips 3×12"),
            ("Tuesday", "Lower: Squats 4×8, RDL 3×10, Leg press 3×12, Calf raises 4×15"),
            ("Thursday", "Upper: Pull-ups 4×6, Incline press 4×8, Curls 3×12, Face pulls 3×15"),
            ("Friday", "Lower: Deadlift 4×5, Lunges 3×10, Leg curls 3×12, Hip thrusts 3×12"),
        ],
    },
    "advanced": {
        "title": "🔴 Advanced Plan (5 days/week — PPL split)",
        "days": [
            ("Monday", "Push: Bench 5×5, OHP 4×6, Incline DB 4×8, Lateral raises 4×15, Triceps 3×12"),
            ("Tuesday", "Pull: Deadlift 5×3, Weighted pull-ups 4×6, Cable rows 4×8, Face pulls 4×15, Curls 3×12"),
            ("Wednesday", "Legs: Squat 5×5, Leg press 4×8, RDL 4×8, Leg curl 4×10, Calf raises 5×15"),
            ("Thursday", "Push: Close-grip bench 4×6, Dips 4×8, DB shoulder 4×10, Cable fly 3×15"),
            ("Friday", "Pull: Rack pulls 4×5, T-bar rows 4×8, Lat pulldown 4×10, Reverse fly 4×15"),
        ],
    },
}
 
 
def _level_keyboard():
    """Inline keyboard for choosing a fitness level."""
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🟢 Beginner", callback_data="workout_beginner"),
        types.InlineKeyboardButton("🟡 Intermediate", callback_data="workout_intermediate"),
        types.InlineKeyboardButton("🔴 Advanced", callback_data="workout_advanced"),
    )
    return markup
 
 
def send_level_menu(bot, message):
    """Ask the user to pick their fitness level."""
    bot.send_message(
        message.chat.id,
        "💪 Choose your fitness level:",
        reply_markup=_level_keyboard(),
    )
 
 
def handle_callback(bot, call):
    """
    Handle inline button presses for workout plans.
    Expects call.data in format 'workout_<level>'.
    """
    level = call.data.split("_", 1)[1]
    plan = PLANS.get(level)
 
    if not plan:
        bot.answer_callback_query(call.id, "Unknown level.")
        return
 
    lines = [f"*{plan['title']}*\n"]
    for day, exercises in plan["days"]:
        lines.append(f"📅 *{day}*\n{exercises}\n")
 
    bot.edit_message_text(
        "\n".join(lines),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown",
    )
    bot.answer_callback_query(call.id, f"{plan['title']} loaded!")