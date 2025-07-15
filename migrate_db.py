#!/usr/bin/env python3
"""
Database migration script to add transaction history table.
Run this script to update existing databases with the new schema.
"""

from database.models import Base, engine
from sqlalchemy import inspect

def main():
    # Create all tables (will only create new ones)
    Base.metadata.create_all(engine)
    
    # Check if the transactions table was created
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if 'transactions' in tables:
        print("✅ Transactions table created successfully!")
    else:
        print("❌ Failed to create transactions table")
    
    print(f"📊 Current tables in database: {', '.join(tables)}")

if __name__ == '__main__':
    main()