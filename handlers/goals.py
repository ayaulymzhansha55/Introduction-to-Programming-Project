"""
handlers/goals.py — Step / Fitness Goal Tracker.
Users set a goal (e.g. "Run 5 km"), mark it done, or reset it.
"""

from telebot import types

# ── In-memory state ───────────────────────────────────────────────────────────
# { chat_id: {"goal": str | None, "done": bool, "awaiting_input": bool} }
_state: dict = {}


def _get_state(chat_id: int) -> dict:
    if chat_id not in _state:
        _state[chat_id] = {"goal": None, "done": False, "awaiting_input": False}
    return _state[chat_id]


# ── Keyboards ─────────────────────────────────────────────────────────────────

def _no_goal_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Set a Goal", callback_data="goal_set"))
    return markup


def _has_goal_keyboard(done: bool) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    if not done:
        markup.add(
            types.InlineKeyboardButton("✅ Mark as Done", callback_data="goal_done"),
            types.InlineKeyboardButton("🔄 Change Goal", callback_data="goal_set"),
        )
    else:
        markup.add(
            types.InlineKeyboardButton("🆕 Set New Goal", callback_data="goal_set"),
        )
    return markup


# ── Public API ────────────────────────────────────────────────────────────────

def is_waiting_for_input(chat_id: int) -> bool:
    """True when we're expecting the user to type their goal."""
    return _get_state(chat_id).get("awaiting_input", False)


def start_goal_tracker(bot, message):
    """Show the current goal status."""
    _send_goal_panel(bot, message.chat.id)


def handle_callback(bot, call):
    """
    Handle inline button presses for goal tracker.
    Expects call.data in format 'goal_<action>'.
    """
    chat_id = call.message.chat.id
    state = _get_state(chat_id)
    action = call.data.split("_", 1)[1]

    if action == "set":
        state["awaiting_input"] = True
        bot.answer_callback_query(call.id)
        bot.send_message(
            chat_id,
            "🎯 What's your fitness goal?\n"
            "_(e.g. Run 5 km, Do 50 push-ups, Walk 10,000 steps)_",
            parse_mode="Markdown",
        )

    elif action == "done":
        state["done"] = True
        bot.answer_callback_query(call.id, "🎉 Awesome! Goal completed!")
        _send_goal_panel(bot, chat_id)

    bot.answer_callback_query(call.id)


def receive_goal_input(bot, message):
    """Save the user's typed goal."""
    chat_id = message.chat.id
    state = _get_state(chat_id)
    state["awaiting_input"] = False

    goal_text = message.text.strip()

    if not goal_text:
        bot.send_message(chat_id, "❌ Goal can't be empty. Try again!")
        return

    if len(goal_text) > 200:
        bot.send_message(chat_id, "❌ Goal is too long (max 200 chars). Please shorten it.")
        return

    state["goal"] = goal_text
    state["done"] = False
    bot.send_message(chat_id, f"✅ Goal set: *{goal_text}*\nYou've got this! 💪", parse_mode="Markdown")
    _send_goal_panel(bot, chat_id)


# ── Internal ──────────────────────────────────────────────────────────────────

def _send_goal_panel(bot, chat_id: int):
    """Send (or refresh) the goal status panel."""
    state = _get_state(chat_id)
    goal = state["goal"]
    done = state["done"]

    if not goal:
        text = "🎯 *Goal Tracker*\n\nYou haven't set a goal yet. Let's fix that!"
        markup = _no_goal_keyboard()
    elif done:
        text = (
            "🎯 *Goal Tracker*\n\n"
            f"Goal: ~~{goal}~~ ✅\n\n"
            "🎉 *Completed! Set a new challenge?*"
        )
        markup = _has_goal_keyboard(done=True)
    else:
        text = (
            "🎯 *Goal Tracker*\n\n"
            f"Current goal: *{goal}*\n"
            "Status: ⏳ In progress...\n\n"
            "Mark it done when you've achieved it!"
        )
        markup = _has_goal_keyboard(done=False)

    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)
