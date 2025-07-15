from telegram import Update
from telegram.ext import ContextTypes
from database.crud import update_debt, get_all_debts, create_transaction, get_transactions
from utils.auth import owner_only
from utils.formatting import format_amount
from datetime import datetime

async def parse_debt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Формат: /команда Имя Сумма")
        return None, None
    
    person_name = ' '.join(context.args[:-1])
    try:
        amount = float(context.args[-1])
        if amount <= 0:
            await update.message.reply_text("Сумма должна быть положительной")
            return None, None
        return person_name, amount
    except ValueError:
        await update.message.reply_text("Неверный формат суммы")
        return None, None

@owner_only
async def borrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person_name, amount = await parse_debt_command(update, context)
    if person_name is None:
        return
    
    user_id = update.message.from_user.id
    update_debt(user_id, person_name, -amount)
    create_transaction(user_id, person_name, -amount, 'borrow')
    
    debts = get_all_debts(user_id)
    current_balance = next((debt.amount for debt in debts if debt.person_name == person_name), 0)
    
    message = f"📝 Записано: вы заняли у {person_name} {format_amount(amount)}\n"
    if current_balance < 0:
        message += f"💸 Теперь вы должны {person_name}: {format_amount(-current_balance)}"
    elif current_balance > 0:
        message += f"💰 Теперь {person_name} должен вам: {format_amount(current_balance)}"
    else:
        message += f"✔️ Взаимные долги с {person_name} погашены"
    
    await update.message.reply_text(message)

@owner_only
async def lend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person_name, amount = await parse_debt_command(update, context)
    if person_name is None:
        return
    
    user_id = update.message.from_user.id
    update_debt(user_id, person_name, amount)
    create_transaction(user_id, person_name, amount, 'lend')
    
    debts = get_all_debts(user_id)
    current_balance = next((debt.amount for debt in debts if debt.person_name == person_name), 0)
    
    message = f"📝 Записано: вы дали взаймы {person_name} {format_amount(amount)}\n"
    if current_balance < 0:
        message += f"💸 Теперь вы должны {person_name}: {format_amount(-current_balance)}"
    elif current_balance > 0:
        message += f"💰 Теперь {person_name} должен вам: {format_amount(current_balance)}"
    else:
        message += f"✔️ Взаимные долги с {person_name} погашены"
    
    await update.message.reply_text(message)

@owner_only
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person_name, amount = await parse_debt_command(update, context)
    if person_name is None:
        return
    
    user_id = update.message.from_user.id
    update_debt(user_id, person_name, amount)
    create_transaction(user_id, person_name, amount, 'pay')
    
    debts = get_all_debts(user_id)
    current_balance = next((debt.amount for debt in debts if debt.person_name == person_name), 0)
    
    message = f"📝 Записано: вы вернули {person_name} {format_amount(amount)}\n"
    if current_balance < 0:
        message += f"💸 Теперь вы должны {person_name}: {format_amount(-current_balance)}"
    elif current_balance > 0:
        message += f"💰 Теперь {person_name} должен вам: {format_amount(current_balance)}"
    else:
        message += f"✔️ Взаимные долги с {person_name} погашены"
    
    await update.message.reply_text(message)

@owner_only
async def returned(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person_name, amount = await parse_debt_command(update, context)
    if person_name is None:
        return
    
    user_id = update.message.from_user.id
    update_debt(user_id, person_name, -amount)
    create_transaction(user_id, person_name, -amount, 'returned')
    
    debts = get_all_debts(user_id)
    current_balance = next((debt.amount for debt in debts if debt.person_name == person_name), 0)
    
    message = f"📝 Записано: {person_name} вернул вам {format_amount(amount)}\n"
    if current_balance < 0:
        message += f"💸 Теперь вы должны {person_name}: {format_amount(-current_balance)}"
    elif current_balance > 0:
        message += f"💰 Теперь {person_name} должен вам: {format_amount(current_balance)}"
    else:
        message += f"✔️ Взаимные долги с {person_name} погашены"
    
    await update.message.reply_text(message)

@owner_only
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    debts = get_all_debts(user_id)
    
    if not debts:
        await update.message.reply_text("У вас нет долгов")
        return
    
    message = "📊 Ваши долги:\n\n"
    total_debt = 0
    
    for debt in debts:
        if debt.amount < 0:
            message += f"💸 {debt.person_name}: {format_amount(-debt.amount)} (вы должны)\n"
        else:
            message += f"💰 {debt.person_name}: {format_amount(debt.amount)} (вам должны)\n"
        total_debt += debt.amount
    
    message += f"\n💰 Итого: {format_amount(abs(total_debt))}"
    if total_debt < 0:
        message += " (вы в долгу)"
    elif total_debt > 0:
        message += " (вам должны)"
    
    await update.message.reply_text(message)

@owner_only
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    person_name = ' '.join(context.args) if context.args else None
    
    transactions = get_transactions(user_id, person_name)
    
    if not transactions:
        if person_name:
            await update.message.reply_text(f"История операций с {person_name} пуста")
        else:
            await update.message.reply_text("История операций пуста")
        return
    
    message = "📜 История операций"
    if person_name:
        message += f" с {person_name}"
    message += ":\n\n"
    
    for transaction in transactions:
        # Format date as requested: "2025 Jul 17, 19:04"
        date_str = transaction.created_at.strftime("%Y %b %d, %H:%M")
        
        # Determine the sign and description based on transaction type
        if transaction.transaction_type == 'borrow':
            # I borrowed money (negative for me)
            amount_str = f"-{format_amount(abs(transaction.amount))}"
            action = "вы заняли у"
        elif transaction.transaction_type == 'lend':
            # I lent money (positive for me)
            amount_str = f"+{format_amount(abs(transaction.amount))}"
            action = "вы дали взаймы"
        elif transaction.transaction_type == 'pay':
            # I paid back (positive for me, reducing my debt)
            amount_str = f"+{format_amount(abs(transaction.amount))}"
            action = "вы вернули"
        elif transaction.transaction_type == 'returned':
            # Someone returned money to me (negative for me, reducing what they owe)
            amount_str = f"-{format_amount(abs(transaction.amount))}"
            action = "вам вернул"
        
        message += f"📅 {date_str}\n"
        message += f"💵 {amount_str} ({action} {transaction.person_name})\n\n"
    
    await update.message.reply_text(message)