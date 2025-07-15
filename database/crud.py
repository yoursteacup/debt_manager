from sqlalchemy.orm import Session
from database.models import Debt, Session as SessionLocal

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