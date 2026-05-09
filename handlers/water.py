"""
handlers/water.py — Water Intake Reminder & Tracker.
Tracks how many glasses of water a user has drunk today.
Goal: 8 glasses per day (configurable via DAILY_GOAL).
"""
from telebot import types
<<<<<<< HEAD

DAILY_GOAL = 8  # glasses per day


# { chat_id: {"glasses": int, "awaiting_input": bool} }
=======
DAILY_GOAL = 8  
>>>>>>> 428586b795a7c7201e8d90a209478695f049cdbf
_state: dict = {}

def _get_state(chat_id: int) -> dict:
    """Return (or create) the water state for a chat."""
    if chat_id not in _state:
        _state[chat_id] = {"glasses": 0, "awaiting_input": False}
    return _state[chat_id]

<<<<<<< HEAD



=======
>>>>>>> 428586b795a7c7201e8d90a209478695f049cdbf
def _progress_bar(glasses: int, goal: int = DAILY_GOAL) -> str:
    """Return a visual progress bar, e.g. '████░░░░ 4/8'."""
    filled = min(glasses, goal)
    bar = "█" * filled + "░" * (goal - filled)
    return f"{bar} {glasses}/{goal}"

def _water_keyboard(glasses: int) -> types.InlineKeyboardMarkup:
    """Inline buttons: +1 glass, +custom, reset."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💧 +1 Glass", callback_data="water_add1"),
        types.InlineKeyboardButton("✏️ Add custom", callback_data="water_custom"),
        types.InlineKeyboardButton("🔄 Reset today", callback_data="water_reset"),
    )
    return markup

<<<<<<< HEAD



=======
>>>>>>> 428586b795a7c7201e8d90a209478695f049cdbf
def is_waiting_for_input(chat_id: int) -> bool:
    """True when we're expecting a free-text number from the user."""
    return _get_state(chat_id).get("awaiting_input", False)

def start_water_tracker(bot, message):
    """Send the water tracker panel."""
    chat_id = message.chat.id
    state = _get_state(chat_id)
    glasses = state["glasses"]

    text = (
        "💧 *Water Intake Tracker*\n\n"
        f"Daily goal: *{DAILY_GOAL} glasses*\n"
        f"Progress: {_progress_bar(glasses)}\n\n"
        "Stay hydrated! 🌊")
    bot.send_message(chat_id,text, parse_mode="Markdown", reply_markup=_water_keyboard(glasses))


def handle_callback(bot, call):
    """
    Handle inline button presses for water tracker.
    Expects call.data in format 'water_<action>'.
    """
    chat_id = call.message.chat.id
    state = _get_state(chat_id)
    action = call.data.split("_", 1)[1]
    if action == "add1":
        state["glasses"] += 1
        _refresh_panel(bot, call, state["glasses"])
    elif action == "custom":
        state["awaiting_input"] = True
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "How many glasses did you drink? (enter a number)")
    elif action == "reset":
        state["glasses"] = 0
        _refresh_panel(bot, call, 0)

    bot.answer_callback_query(call.id)


def receive_water_input(bot, message):
    """Process free-text number input for custom glasses."""
    chat_id = message.chat.id
    state = _get_state(chat_id)
    state["awaiting_input"] = False

    try:
        amount = int(message.text.strip())
        if amount < 0:
            raise ValueError("Negative number")
        state["glasses"] += amount
        glasses = state["glasses"]
        emoji = "🎉" if glasses >= DAILY_GOAL else "💧"
        bot.send_message(
            chat_id,
            f"{emoji} Added *{amount}* glass(es)!\n"
            f"Total today: {_progress_bar(glasses)}",
            parse_mode="Markdown",
            reply_markup=_water_keyboard(glasses),
        )
    except ValueError:
        bot.send_message(
            chat_id,
            "❌ Please enter a valid whole number (e.g. 2).",
        )

def _refresh_panel(bot, call, glasses: int):
    """Edit the existing message to reflect the new glass count."""
    reached = glasses >= DAILY_GOAL
    status = "🎉 *Goal reached! Amazing work!*" if reached else "Keep going! 💪"
    text = (
        "💧 *Water Intake Tracker*\n\n"
        f"Daily goal: *{DAILY_GOAL} glasses*\n"
        f"Progress: {_progress_bar(glasses)}\n\n"
        f"{status}"
    )
    try:
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=_water_keyboard(glasses),
        )
    except Exception:
        pass 
