from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from typing import List, Dict
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

@router.get("/monthly-trend")
async def get_monthly_trend(
    months: int = 6,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get monthly income and expense trends"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    # Get all transactions in the period
    transactions = db.query(
        extract('year', models.Transaction.date).label('year'),
        extract('month', models.Transaction.date).label('month'),
        models.Transaction.type,
        func.sum(models.Transaction.amount).label('total')
    ).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.date >= start_date
    ).group_by(
        extract('year', models.Transaction.date),
        extract('month', models.Transaction.date),
        models.Transaction.type
    ).all()
    
    # Organize data by month
    monthly_data = {}
    current = datetime.now()
    
    for i in range(months):
        month_date = datetime(current.year, current.month, 1) - timedelta(days=i * 30)
        month_key = f"{month_date.year}-{month_date.month:02d}"
        monthly_data[month_key] = {
            "income": 0,
            "expenses": 0,
            "month": month_date.strftime("%b %Y")
        }
    
    # Fill in actual data
    for year, month, trans_type, total in transactions:
        month_key = f"{int(year)}-{int(month):02d}"
        if month_key in monthly_data:
            if trans_type == models.TransactionType.INCOME:
                monthly_data[month_key]["income"] = float(total)
            else:
                monthly_data[month_key]["expenses"] = float(total)
    
    # Convert to list and sort by date
    result = sorted(
        [{"month": v["month"], "income": v["income"], "expenses": v["expenses"], "savings": v["income"] - v["expenses"]} 
         for v in monthly_data.values()],
        key=lambda x: x["month"]
    )
    
    return result

@router.get("/spending-by-category")
async def get_spending_by_category(
    months: int = 1,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get spending breakdown by category for specified months"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    breakdown = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label('total'),
        func.count(models.Transaction.id).label('count')
    ).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.type == models.TransactionType.EXPENSE,
        models.Transaction.date >= start_date
    ).group_by(models.Transaction.category).all()
    
    total_expenses = sum(total for _, total, _ in breakdown)
    
    return [
        {
            "category": cat,
            "amount": float(total),
            "percentage": (float(total) / total_expenses * 100) if total_expenses > 0 else 0,
            "count": count
        }
        for cat, total, count in breakdown if cat
    ]