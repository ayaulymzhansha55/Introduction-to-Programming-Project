"""
handlers/goals.py - Step/Fitness Goal Tracker. 
Users set a goal (e.g. "Run 5km"), mark it done or reset it. 
"""
from telebot import types 
_state: dict = {}
def _get_state(chat_id: int) -> dict:
    if chat_id not in _state:
        _state(chat_id) = {"goal": None, "done": False, "awaiting_input": False}
    return _state[chat_id]
def _no_goal_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Set Goal", callback_data="goal_set"))
    return markup
def _has_goal_keyboard(done: bool) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    if not done:
        markup.add(types.InlineKeyboardButton("✅ Mark as Done", callback_data="goal_done"), types.InlineKeyboardButton("🔄 Change Goal", callback_data="goal_set"))
    else:
        markup.add(types.InlineKeyboardButton("🆕 Set New Goal", callback_data="goal_set"))
    return markup
def is_waiting_for_input(chat_id: int) ->bool:
    """True when we're expecting the user to type their goal."""
    return _get_state(chat_id).get("awaiting_input", False)
def start_goal_tracker()