from telegram import Update
from telegram.ext import ContextTypes
from database.crud import update_debt, get_all_debts
from utils.auth import owner_only
from utils.formatting import format_amount

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