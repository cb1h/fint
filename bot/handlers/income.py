from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.models.database import SessionLocal, Transaction
from datetime import datetime, timedelta
from config import ADMIN_USER_ID


class IncomeStates(StatesGroup):
    waiting_for_source = State()
    waiting_for_method = State()
    waiting_for_date = State()
    waiting_for_amount = State()


async def income_command(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    sources = ["Salary", "Projects", "Other"]
    source_buttons = [KeyboardButton(text=source) for source in sources]
    source_markup = ReplyKeyboardMarkup(keyboard=[source_buttons], resize_keyboard=True)

    await message.answer("Select the income source:", reply_markup=source_markup)
    await state.set_state(IncomeStates.waiting_for_source)


async def select_method(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    await state.update_data(source=message.text)

    methods = ["Cash", "Card"]
    method_buttons = [KeyboardButton(text=method) for method in methods]
    method_markup = ReplyKeyboardMarkup(keyboard=[method_buttons], resize_keyboard=True)

    await message.answer("Select the method:", reply_markup=method_markup)
    await state.set_state(IncomeStates.waiting_for_method)


async def select_date(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    await state.update_data(method=message.text)

    today = datetime.today()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    date_buttons = [KeyboardButton(text=date) for date in dates]
    date_markup = ReplyKeyboardMarkup(keyboard=[date_buttons], resize_keyboard=True)

    await message.answer("Select the date:", reply_markup=date_markup)
    await state.set_state(IncomeStates.waiting_for_date)


async def select_amount(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    await state.update_data(date=message.text)

    await message.answer("Please enter the amount:")
    await state.set_state(IncomeStates.waiting_for_amount)


async def add_income(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("Access denied.")
        return

    session = None
    try:
        user_data = await state.get_data()
        source = user_data['source']
        method = user_data['method']
        date_str = user_data['date']
        amount_str = message.text

        date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        amount = float(amount_str.strip())

        session = SessionLocal()
        transaction = Transaction(
            user_id=message.from_user.id,
            type='income',
            category=source.strip(),
            method=method.strip(),
            date=date,
            amount=amount
        )
        session.add(transaction)
        session.commit()
        await message.answer("Income added successfully!")
    except Exception as e:
        await message.answer(f"Error: {e}")
    finally:
        if session:
            session.close()
        await state.clear()


def register_handlers_income(dp: Dispatcher):
    dp.message.register(income_command, Command(commands=['income']))
    dp.message.register(select_method, IncomeStates.waiting_for_source)
    dp.message.register(select_date, IncomeStates.waiting_for_method)
    dp.message.register(select_amount, IncomeStates.waiting_for_date)
    dp.message.register(add_income, IncomeStates.waiting_for_amount)