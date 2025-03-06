# bot/handlers/report.py

from aiogram import types, Dispatcher
from aiogram.filters import Command
from bot.models.database import SessionLocal, Transaction, User
from datetime import datetime, timedelta
from config import ADMIN_USER_ID


async def report_command(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    session = None
    try:
        session = SessionLocal()
        user_id = message.from_user.id
        today = datetime.today()
        week_start = today - timedelta(days=today.weekday() + 1)

        incomes = session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'income',
            Transaction.date >= week_start
        ).all()
        expenses = session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.date >= week_start
        ).all()

        total_income = sum(t.amount for t in incomes)
        total_expense = sum(t.amount for t in expenses)

        user = session.query(User).filter(User.telegram_id == user_id).first()
        if user is None:
            user = User(telegram_id=user_id, cash_balance=0.0, card_balance=0.0)
            session.add(user)
            session.commit()

        savings = user.cash_balance + user.card_balance + total_income - total_expense

        report = (
            f"Weekly Report:\n"
            f"Savings: {savings}\n"
            f"Total Weekly Income: {total_income}\n"
            f"Total Weekly Expense: {total_expense}"
        )

        await message.answer(report)
    except Exception as e:
        await message.answer(f"Error: {e}")
    finally:
        if session:
            session.close()


def register_handlers_report(dp: Dispatcher):
    dp.message.register(report_command, Command(commands=['report']))