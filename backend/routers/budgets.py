from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
import models
import schemas
import auth

router = APIRouter()

@router.post("/", response_model=schemas.Budget)
async def create_budget(
    budget: schemas.BudgetCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if budget exists for this category and month
    existing_budget = db.query(models.Budget).filter(
        models.Budget.user_id == current_user.id,
        models.Budget.category_id == budget.category_id,
        models.Budget.month == budget.month,
        models.Budget.year == budget.year
    ).first()
    
    if existing_budget:
        # Update existing budget
        existing_budget.amount = budget.amount
        existing_budget.is_active = budget.is_active
        db.commit()
        db.refresh(existing_budget)
        return existing_budget
    
    # Create new budget
    db_budget = models.Budget(
        **budget.dict(),
        user_id=current_user.id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/", response_model=List[schemas.Budget])
async def read_budgets(
    month: int = None,
    year: int = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year
    
    budgets = db.query(models.Budget).filter(
        models.Budget.user_id == current_user.id,
        models.Budget.month == month,
        models.Budget.year == year
    ).all()
    return budgets

@router.get("/{budget_id}", response_model=schemas.Budget)
async def read_budget(
    budget_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.put("/{budget_id}", response_model=schemas.Budget)
async def update_budget(
    budget_id: int,
    budget_update: schemas.BudgetCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    for key, value in budget_update.dict().items():
        setattr(budget, key, value)
    
    db.commit()
    db.refresh(budget)
    return budget

@router.delete("/{budget_id}")
async def delete_budget(
    budget_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(budget)
    db.commit()
    return {"detail": "Budget deleted"}