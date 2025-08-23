from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from database import get_db
import models
import schemas
import auth

router = APIRouter()

@router.get("/stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Calculate totals
    total_income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.INCOME
    ).scalar() or 0
    
    total_expenses = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.EXPENSE
    ).scalar() or 0
    
    # Calculate monthly totals
    current_month = datetime.now().month
    current_year = datetime.now().year
    month_start = datetime(current_year, current_month, 1)
    
    monthly_income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.INCOME,
        models.Transaction.date >= month_start
    ).scalar() or 0
    
    monthly_expenses = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.EXPENSE,
        models.Transaction.date >= month_start
    ).scalar() or 0
    
    # Goals statistics
    active_goals = db.query(func.count(models.Goal.id)).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.is_active == True
    ).scalar() or 0
    
    goals = db.query(models.Goal).filter(
        models.Goal.user_id == current_user.id,
        models.Goal.is_active == True
    ).all()
    
    total_goals_progress = 0
    if goals:
        total_target = sum(g.target_amount for g in goals)
        total_current = sum(g.current_amount for g in goals)
        total_goals_progress = (total_current / total_target * 100) if total_target > 0 else 0
    
    # Budget utilization
    budgets = db.query(models.Budget).filter(
        models.Budget.user_id == current_user.id,
        models.Budget.month == current_month,
        models.Budget.year == current_year
    ).all()
    
    budget_utilization = 0
    if budgets:
        total_limit = sum(b.amount for b in budgets)
        total_spent = sum(b.spent for b in budgets)
        budget_utilization = (total_spent / total_limit * 100) if total_limit > 0 else 0
    
    return schemas.DashboardStats(
        total_income=total_income,
        total_expenses=total_expenses,
        balance=total_income - total_expenses,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        active_goals=active_goals,
        total_goals_progress=total_goals_progress,
        budget_utilization=budget_utilization
    )

@router.get("/recent-transactions")
async def get_recent_transactions(
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).order_by(models.Transaction.date.desc()).limit(limit).all()
    return transactions

@router.get("/category-breakdown")
async def get_category_breakdown(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    current_month = datetime.now().month
    current_year = datetime.now().year
    month_start = datetime(current_year, current_month, 1)
    
    breakdown = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label('total')
    ).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.EXPENSE,
        models.Transaction.date >= month_start
    ).group_by(models.Transaction.category).all()
    
    return {cat: total for cat, total in breakdown if cat}