def format_amount(amount: float) -> str:
    """Форматирует сумму с разделителями тысяч и символом тенге"""
    amount_int = int(amount)
    formatted = f"{amount_int:,}".replace(",", "'")
    return f"{formatted}₸"