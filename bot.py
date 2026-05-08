"""
FitBot - A Telegram Fitness Bot
Main entry point. Registers all handlers and starts polling.
"""

import telebot
from telebot import types
import os

from config import BOT_TOKEN
from handlers import workout, water, goals, quote


bot = telebot.TeleBot(BOT_TOKEN)


# ── Main Menu ────────────────────────────────────────────────────────────────

def main_menu_keyboard():
    """Return the main menu inline keyboard."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🏋️ Workout Plans"),
        types.KeyboardButton("💧 Water Reminder"),
        types.KeyboardButton("🎯 Goal Tracker"),
        types.KeyboardButton("✨ Daily Quote"),
    )
    return markup


@bot.message_handler(commands=["start"])
def handle_start(message):
    """Greet the user and show the main menu."""
    name = message.from_user.first_name or "Athlete"
    bot.send_message(
        message.chat.id,
        f"👋 Hey, *{name}*! Welcome to *FitBot* 💪\n\n"
        "I'm your personal fitness assistant. Choose what you'd like to do:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["help"])
def handle_help(message):
    """Show available commands."""
    bot.send_message(
        message.chat.id,
        "🤖 *FitBot Commands*\n\n"
        "🏋️ *Workout Plans* — Get a plan by fitness level\n"
        "💧 *Water Reminder* — Track your daily water intake\n"
        "🎯 *Goal Tracker* — Set and track a fitness goal\n"
        "✨ *Daily Quote* — Get a motivational fitness quote\n\n"
        "Use /start to go back to the main menu.",
        parse_mode="Markdown",
    )


# ── Route keyboard buttons ────────────────────────────────────────────────────

@bot.message_handler(func=lambda m: m.text == "🏋️ Workout Plans")
def route_workout(message):
    workout.send_level_menu(bot, message)


@bot.message_handler(func=lambda m: m.text == "💧 Water Reminder")
def route_water(message):
    water.start_water_tracker(bot, message)


@bot.message_handler(func=lambda m: m.text == "🎯 Goal Tracker")
def route_goals(message):
    goals.start_goal_tracker(bot, message)


@bot.message_handler(func=lambda m: m.text == "✨ Daily Quote")
def route_quote(message):
    quote.send_quote(bot, message)


# ── Callback query router ─────────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda call: call.data.startswith("workout_"))
def handle_workout_callback(call):
    workout.handle_callback(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("water_"))
def handle_water_callback(call):
    water.handle_callback(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("goal_"))
def handle_goal_callback(call):
    goals.handle_callback(bot, call)


@bot.callback_query_handler(func=lambda call: call.data == "quote_refresh")
def handle_quote_callback(call):
    quote.handle_refresh_callback(bot, call)


# ── Conversation state handler ────────────────────────────────────────────────

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    """Catch-all: route free-text to whichever feature is waiting for input."""
    chat_id = message.chat.id

    if goals.is_waiting_for_input(chat_id):
        goals.receive_goal_input(bot, message)
    elif water.is_waiting_for_input(chat_id):
        water.receive_water_input(bot, message)
    else:
        bot.send_message(
            chat_id,
            "Please choose an option from the menu below 👇",
            reply_markup=main_menu_keyboard(),
        )


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🤖 FitBot is running...")
    bot.infinity_polling()
