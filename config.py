"""
Configuration file for the Fitness Bot.
Store sensitive values in environment variables or a .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
