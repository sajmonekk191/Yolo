from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
import models
import schemas
import auth

router = APIRouter()

# Mapování category_id na názvy kategorií (podle API /categories)
CATEGORY_NAMES = {
    1: "Mzda",
    2: "Freelance",
    3: "Investice",
    4: "Dary",
    5: "Ostatní příjmy",
    6: "Jídlo a potraviny",
    7: "Bydlení",
    8: "Doprava",
    9: "Zdraví",
    10: "Oblečení",
    11: "Zábava",
    12: "Restaurace",
    13: "Sport",
    14: "Cestování",
    15: "Vzdělání",
    16: "Telefon a internet",
    17: "Pojištění",
    18: "Energie",
    19: "Předplatné",
    20: "Ostatní výdaje"
}

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
        existing_budget.category = CATEGORY_NAMES.get(existing_budget.category_id, f"Kategorie {existing_budget.category_id}")
        return existing_budget
    
    # Create new budget
    db_budget = models.Budget(
        **budget.dict(),
        user_id=current_user.id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    db_budget.category = CATEGORY_NAMES.get(db_budget.category_id, f"Kategorie {db_budget.category_id}")
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
    
    # Přidáme název kategorie ke každému rozpočtu
    for budget in budgets:
        budget.category = CATEGORY_NAMES.get(budget.category_id, f"Kategorie {budget.category_id}")
    
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