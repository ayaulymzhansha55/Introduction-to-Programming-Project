"""
handlers/quote.py — Daily Motivational Fitness Quote (creative feature).
Sends a random quote with a fun fitness emoji theme.
"""

import random
from telebot import types



    QUOTES = [
    ("The only bad workout is the one that didn't happen.", "Unknown"),
    ("Take care of your body. It's the only place you have to live.", "Jim Rohn"),
    ("Fitness is not about being better than someone else. It's about being better than you used to be.", "Khloe Kardashian"),
    ("The pain you feel today will be the strength you feel tomorrow.", "Arnold Schwarzenegger"),
    ("Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
    ("All progress takes place outside the comfort zone.", "Michael John Bobak"),
    ("If it doesn't challenge you, it doesn't change you.", "Fred DeVito"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("The hardest lift of all is lifting your butt off the couch.", "Unknown"),
    ("Your body can stand almost anything. It's your mind that you have to convince.", "Unknown"),
    ("Sweat is just fat crying.", "Unknown"),
    ("Don't wish for a good body, work for it.", "Unknown"),
    ("Sore today, strong tomorrow.", "Unknown"),
    ("Dead last finish is greater than did not finish, which beats did not start.", "Unknown"),
    ("The difference between try and triumph is a little 'umph'.", "Marvin Phillips"),
    ("No matter how slow you go, you are still lapping everybody on the couch.", "Unknown"),
    ("Motivation is what gets you started. Habit is what keeps you going.", "Jim Ryun"),
    ("Strive for progress, not perfection.", "Unknown"),
    ("Train insane or remain the same.", "Unknown"),
    ("Your only limit is you.", "Unknown"),
]

EMOJIS = ["🔥", "💪", "🏆", "⚡", "🚀", "🌟", "🎯", "🦾", "💥", "🏅"]




def send_quote(bot, message):
    """Send a random motivational fitness quote."""
    quote_text, author = random.choice(QUOTES)
    emoji = random.choice(EMOJIS)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔁 Another Quote", callback_data="quote_refresh"))

    bot.send_message(
        message.chat.id,
        f"{emoji} *Daily Fitness Quote*\n\n"
        f'_"{quote_text}"_\n\n'
        f"— {author}",
        parse_mode="Markdown",
        reply_markup=markup,
    )


def handle_refresh_callback(bot, call):
    """Handle the 'Another Quote' button."""
    quote_text, author = random.choice(QUOTES)
    emoji = random.choice(EMOJIS)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔁 Another Quote", callback_data="quote_refresh"))

    try:
        bot.edit_message_text(
            f"{emoji} *Daily Fitness Quote*\n\n"
            f'_"{quote_text}"_\n\n'
            f"— {author}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup,
        )
    except Exception:
        pass

    bot.answer_callback_query(call.id, "Here's another one! 💪")
