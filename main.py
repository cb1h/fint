import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN
from bot.handlers import start, income, expense, report
from bot.utils.scheduler import schedule_weekly_report

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрация хендлеров
start.register_handlers_start(dp)
income.register_handlers_income(dp)
expense.register_handlers_expense(dp)
report.register_handlers_report(dp)

async def main():
    await schedule_weekly_report(dp)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())