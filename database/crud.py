from sqlalchemy.orm import Session
from database.models import Debt, Transaction, Session as SessionLocal

def get_or_create_debt(user_id: int, person_name: str) -> Debt:
    session = SessionLocal()
    debt = session.query(Debt).filter_by(
        user_id=user_id, 
        person_name=person_name
    ).first()
    
    if not debt:
        debt = Debt(user_id=user_id, person_name=person_name, amount=0)
        session.add(debt)
        session.commit()
    
    session.close()
    return debt

def update_debt(user_id: int, person_name: str, amount_change: float):
    session = SessionLocal()
    debt = session.query(Debt).filter_by(
        user_id=user_id, 
        person_name=person_name
    ).first()
    
    if debt:
        debt.amount += amount_change
        if abs(debt.amount) < 0.01:
            session.delete(debt)
        session.commit()
    else:
        debt = Debt(user_id=user_id, person_name=person_name, amount=amount_change)
        session.add(debt)
        session.commit()
    
    session.close()

def get_all_debts(user_id: int):
    session = SessionLocal()
    debts = session.query(Debt).filter_by(user_id=user_id).all()
    session.close()
    return debts

def create_transaction(user_id: int, person_name: str, amount: float, transaction_type: str):
    session = SessionLocal()
    transaction = Transaction(
        user_id=user_id,
        person_name=person_name,
        amount=amount,
        transaction_type=transaction_type
    )
    session.add(transaction)
    session.commit()
    session.close()

def get_transactions(user_id: int, person_name: str = None):
    session = SessionLocal()
    query = session.query(Transaction).filter_by(user_id=user_id)
    
    if person_name:
        query = query.filter_by(person_name=person_name)
    
    transactions = query.order_by(Transaction.created_at.desc()).all()
    session.close()
    return transactions