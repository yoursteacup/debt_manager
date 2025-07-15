from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class Debt(Base):
    __tablename__ = 'debts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    person_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<Debt(user_id={self.user_id}, person_name='{self.person_name}', amount={self.amount})>"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)