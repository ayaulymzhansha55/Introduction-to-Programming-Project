# 🤖 FitBot — Telegram Fitness Assistant

A Telegram bot that helps users stay fit and motivated through workout plans, water intake tracking, goal setting, and daily motivational quotes.

Built with Python and [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏋️ **Workout Plans** | Beginner / Intermediate / Advanced weekly training plans |
| 💧 **Water Reminder** | Track daily water intake with a visual progress bar |
| 🎯 **Goal Tracker** | Set a personal fitness goal and mark it complete |
| ✨ **Daily Quote** | Random motivational fitness quotes with a refresh button |

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher → [python.org](https://python.org)
- A Telegram account

### 2. Get your Bot Token
1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the steps
3. Copy the token you receive (looks like `7123456789:AAFxxx...`)

### 3. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/fitness-bot.git
cd fitness-bot
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Add your token
Open `config.py` and paste your token:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

### 6. Run the bot
```bash
python bot.py
```

You should see: `🤖 FitBot is running...`  
Open Telegram, find your bot, and send `/start`!

---

## 📁 Project Structure

```
fitness-bot/
├── bot.py              # Entry point — registers all handlers
├── config.py           # Bot token configuration
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── handlers/
    ├── __init__.py
    ├── workout.py      # Workout Plans feature
    ├── water.py        # Water Intake Tracker
    ├── goals.py        # Goal Tracker
    └── quote.py        # Daily Motivational Quote
```

---

## 👥 Team Members

| Name | Contribution |
|---|---|
| Alkeeva Dilyara | `handlers/workout.py`, bot structure |
| Zhansha Ayaulym | `handlers/water.py`, `handlers/goals.py` |
| Gani Aruzhan | `handlers/quote.py`, README, testing |

---

## 🛠 Dependencies

- `pyTelegramBotAPI==4.21.0` — Telegram Bot API wrapper

---

## 📝 Notes

- Data is stored in-memory (resets when bot restarts). A database like SQLite can be added for persistence.
- The bot uses long-polling (`infinity_polling`) for simplicity.
