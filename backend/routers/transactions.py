from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from database import get_db
import models
import schemas
import auth
from .categories import CATEGORIES

router = APIRouter()

def get_category_info(category_id: int) -> Optional[Dict[str, Any]]:
    """Helper function to get category information"""
    return next((cat for cat in CATEGORIES if cat["id"] == category_id), None)

@router.post("/", response_model=schemas.Transaction)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Zpracovat datum správně - pokud není čas, použít aktuální čas v lokální zóně
    transaction_data = transaction.dict()
    if transaction_data.get('date'):
        # Pokud je datum string bez času, přidáme aktuální čas
        if isinstance(transaction_data['date'], str):
            transaction_data['date'] = datetime.fromisoformat(transaction_data['date'])
    
    db_transaction = models.Transaction(
        **transaction_data,
        user_id=current_user.id
    )
    db.add(db_transaction)
    
    # Update budget if expense
    if transaction.type == models.TransactionType.EXPENSE and transaction.category_id:
        current_month = datetime.now().month
        current_year = datetime.now().year
        budget = db.query(models.Budget).filter(
            models.Budget.user_id == current_user.id,
            models.Budget.category_id == transaction.category_id,
            models.Budget.month == current_month,
            models.Budget.year == current_year
        ).first()
        if budget:
            budget.spent += transaction.amount
    
    db.commit()
    db.refresh(db_transaction)
    
    # Přidat informace o kategorii
    result = schemas.Transaction.model_validate(db_transaction)
    if db_transaction.category_id:
        result.category = get_category_info(db_transaction.category_id)
    return result

@router.get("/", response_model=List[schemas.Transaction])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    type: Optional[models.TransactionType] = None,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)
    
    if type:
        query = query.filter(models.Transaction.type == type)
    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    
    transactions = query.order_by(models.Transaction.id.desc()).offset(skip).limit(limit).all()
    
    # Přidat informace o kategorii ke každé transakci
    result = []
    for transaction in transactions:
        trans_dict = schemas.Transaction.model_validate(transaction)
        if transaction.category_id:
            trans_dict.category = get_category_info(transaction.category_id)
        result.append(trans_dict)
    
    return result

@router.get("/{transaction_id}", response_model=schemas.Transaction)
async def read_transaction(
    transaction_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Přidat informace o kategorii
    result = schemas.Transaction.model_validate(transaction)
    if transaction.category_id:
        result.category = get_category_info(transaction.category_id)
    return result

@router.put("/{transaction_id}", response_model=schemas.Transaction)
async def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    for key, value in transaction_update.dict().items():
        setattr(transaction, key, value)
    
    db.commit()
    db.refresh(transaction)
    
    # Přidat informace o kategorii
    result = schemas.Transaction.model_validate(transaction)
    if transaction.category_id:
        result.category = get_category_info(transaction.category_id)
    return result

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted"}