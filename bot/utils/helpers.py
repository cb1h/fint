# bot/utils/helpers.py

def calculate_savings(cash_balance, card_balance, incomes, expenses):
    return cash_balance + card_balance + sum(incomes) - sum(expenses)

def calculate_weekly_totals(transactions, transaction_type):
    return sum(t.amount for t in transactions if t.type == transaction_type)

