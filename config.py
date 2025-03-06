import os

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///fint.db')

# Report schedule
REPORT_DAY = 6  # Sunday
REPORT_TIME = '20:00'  # 8 PM

# Admin user ID
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))