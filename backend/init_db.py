#!/usr/bin/env python3
from database import engine, SessionLocal
from models import User, Transaction, Goal, Budget, TransactionType, ExpenseCategory, Frequency
from auth import get_password_hash
from datetime import datetime, timedelta
import random

# Create all tables
from database import Base
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✨ Inicializace databáze...")

# Create a session
db = SessionLocal()

try:
    # Create demo user
    demo_user = User(
        email="demo@yolo-finance.cz",
        username="Demo User",
        hashed_password=get_password_hash("demo123"),
        is_active=True
    )
    db.add(demo_user)
    db.commit()
    print(f"✅ Demo uživatel vytvořen: {demo_user.email}")
    
    # Create sample income transactions
    incomes = [
        {"description": "Výplata", "amount": 45000, "date": datetime.now() - timedelta(days=5)},
        {"description": "Freelance projekt", "amount": 25000, "date": datetime.now() - timedelta(days=10)},
        {"description": "Investiční výnos", "amount": 3500, "date": datetime.now() - timedelta(days=15)},
    ]
    
    for income_data in incomes:
        transaction = Transaction(
            user_id=demo_user.id,
            type=TransactionType.INCOME,
            amount=income_data["amount"],
            description=income_data["description"],
            date=income_data["date"]
        )
        db.add(transaction)
    
    # Create sample expense transactions
    expenses = [
        {"description": "Nájem", "amount": 15000, "category": ExpenseCategory.HOUSING},
        {"description": "Nákup potravin", "amount": 3500, "category": ExpenseCategory.FOOD},
        {"description": "Benzín", "amount": 2000, "category": ExpenseCategory.TRANSPORT},
        {"description": "Elektřina", "amount": 1800, "category": ExpenseCategory.UTILITIES},
        {"description": "Netflix", "amount": 300, "category": ExpenseCategory.ENTERTAINMENT},
        {"description": "Oběd v restauraci", "amount": 450, "category": ExpenseCategory.FOOD},
    ]
    
    for expense_data in expenses:
        transaction = Transaction(
            user_id=demo_user.id,
            type=TransactionType.EXPENSE,
            amount=expense_data["amount"],
            description=expense_data["description"],
            category=expense_data["category"],
            date=datetime.now() - timedelta(days=random.randint(1, 20))
        )
        db.add(transaction)
    
    # Create sample goals
    goals = [
        {"name": "Nové auto", "target_amount": 300000, "current_amount": 75000},
        {"name": "Dovolená v Thajsku", "target_amount": 50000, "current_amount": 20000},
        {"name": "Rezervní fond", "target_amount": 100000, "current_amount": 35000},
    ]
    
    for goal_data in goals:
        goal = Goal(
            user_id=demo_user.id,
            name=goal_data["name"],
            target_amount=goal_data["target_amount"],
            current_amount=goal_data["current_amount"],
            deadline=datetime.now() + timedelta(days=365),
            is_active=True
        )
        db.add(goal)
    
    # Create sample budgets for current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    budgets = [
        {"category": ExpenseCategory.FOOD, "monthly_limit": 8000, "current_spent": 3950},
        {"category": ExpenseCategory.TRANSPORT, "monthly_limit": 3000, "current_spent": 2000},
        {"category": ExpenseCategory.ENTERTAINMENT, "monthly_limit": 2000, "current_spent": 300},
        {"category": ExpenseCategory.UTILITIES, "monthly_limit": 3000, "current_spent": 1800},
    ]
    
    for budget_data in budgets:
        budget = Budget(
            user_id=demo_user.id,
            category=budget_data["category"],
            monthly_limit=budget_data["monthly_limit"],
            current_spent=budget_data["current_spent"],
            month=current_month,
            year=current_year
        )
        db.add(budget)
    
    db.commit()
    print("✅ Testovací data vytvořena")
    
    # Print summary
    print("\n📊 Souhrn dat:")
    print(f"   - Příjmy: {len(incomes)} transakcí")
    print(f"   - Výdaje: {len(expenses)} transakcí")
    print(f"   - Cíle: {len(goals)} aktivních")
    print(f"   - Rozpočty: {len(budgets)} kategorií")
    
except Exception as e:
    print(f"❌ Chyba: {e}")
    db.rollback()
finally:
    db.close()

print("\n🚀 Databáze je připravena!")
print("   Email: demo@yolo-finance.cz")
print("   Heslo: demo123")