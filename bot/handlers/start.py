from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_USER_ID
from bot.models.database import SessionLocal, User


async def start_command(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
    if user is None:
        user = User(telegram_id=message.from_user.id, cash_balance=0.0, card_balance=0.0)
        session.add(user)
        session.commit()
    session.close()

    await message.answer("Welcome to your personal finance tracker bot! Use /help to see available commands.")


async def help_command(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    help_text = (
        "/start - Start the bot\n"
        "/setbalance - Set initial balance\n"
        "Balance: <cash_balance>, <card_balance> - Update balance\n"
        "/income - Add income\n"
        "/expense - Add expense\n"
        "/report - Get weekly report\n"
    )
    await message.answer(help_text)


async def set_balance_command(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    await message.answer("Please provide the balance details in the following format:\nCash Balance, Card Balance")


async def update_balance(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    session = None
    try:
        # Удаляем префикс "Balance: " и разбиваем строку на две части
        balance_str = message.text.replace('Balance: ', '')
        cash_balance, card_balance = map(float, balance_str.split(','))
        
        session = SessionLocal()
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
        if user is None:
            user = User(telegram_id=message.from_user.id, cash_balance=cash_balance, card_balance=card_balance)
            session.add(user)
        else:
            user.cash_balance = cash_balance
            user.card_balance = card_balance
        session.commit()
        await message.answer("Balance updated successfully!")
    except Exception as e:
        await message.answer(f"Error: {e}")
    finally:
        if session:
            session.close()


def register_handlers_start(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=['start']))
    dp.message.register(help_command, Command(commands=['help']))
    dp.message.register(set_balance_command, Command(commands=['setbalance']))
    dp.message.register(update_balance, lambda message: message.text.startswith('Balance:'))