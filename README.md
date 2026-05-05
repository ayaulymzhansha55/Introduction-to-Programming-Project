# 🏋️ FitBot — Fitness Telegram Bot

A feature-rich Telegram bot for tracking workouts, browsing exercise tips, and logging fitness progress.

---

## Features

| Command | Description |
|---|---|
| `/start` | Welcome message and main menu |
| `/workout` | Browse beginner, intermediate, and cardio plans |
| `/exercise` | Explore the exercise library by muscle group |
| `/log` | Log a workout session |
| `/progress` | View your last 10 logged workouts |

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ayaulymzhansha55/Introduction-to-Programming-Project.git
cd Introduction-to-Programming-Project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the bot token

```bash
cp .env.example .env
```

Open `.env` and paste your token from [@BotFather](https://t.me/BotFather):

```
BOT_TOKEN=your_telegram_bot_token_here
```

> ⚠️ **Never commit your `.env` file** — it's listed in `.gitignore`.

### 5. Run the bot

```bash
python main.py
```

---

## Project Structure

```
fitness_bot/
├── main.py              # Entry point — registers all handlers
├── config.py            # Loads BOT_TOKEN from environment
├── database.py          # SQLite database setup and queries
├── handlers/
│   ├── __init__.py
│   ├── start.py         # /start command
│   ├── workout.py       # /workout command + inline callbacks
│   ├── exercise.py      # /exercise command + inline callbacks
│   └── progress.py      # /log and /progress commands
├── requirements.txt     # Project dependencies
├── .env.example         # Token template (safe to commit)
├── .gitignore           # Excludes .env and database files
└── README.md
```

---

## How to Log a Workout

```
/log <exercise> <sets> <reps> [weight_kg] [notes]
```

**Examples:**

```
/log Squat 4 8 100
/log Plank 3 60 0 felt really stable today
/log "Bench Press" 3 10 75
```

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `python-telegram-bot` | 21.3 | Telegram Bot API wrapper |
| `python-dotenv` | 1.0.1 | Load `.env` variables |

SQLite is used for the database — no extra installation needed (built into Python).

---

## Team Members

- Member 1 — ...
- Member 2 — ...
- Member 3 — ...
