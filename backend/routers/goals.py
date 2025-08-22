from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
import models
import schemas
import auth

router = APIRouter()

@router.post("/", response_model=schemas.Goal)
async def create_goal(
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_goal = models.Goal(
        **goal.dict(),
        user_id=current_user.id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/", response_model=List[schemas.Goal])
async def read_goals(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Goal).filter(models.Goal.user_id == current_user.id)
    if active_only:
        query = query.filter(models.Goal.is_active == True)
    goals = query.offset(skip).limit(limit).all()
    return goals

@router.get("/{goal_id}", response_model=schemas.Goal)
async def read_goal(
    goal_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.put("/{goal_id}", response_model=schemas.Goal)
async def update_goal(
    goal_id: int,
    goal_update: schemas.GoalUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    if goal_update.current_amount is not None:
        goal.current_amount = goal_update.current_amount
        if goal.current_amount >= goal.target_amount:
            goal.is_active = False
            goal.completed_at = datetime.utcnow()
    
    if goal_update.is_active is not None:
        goal.is_active = goal_update.is_active
    
    db.commit()
    db.refresh(goal)
    return goal

@router.post("/{goal_id}/contribute", response_model=schemas.Goal)
async def contribute_to_goal(
    goal_id: int,
    amount: float,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    goal.current_amount += amount
    if goal.current_amount >= goal.target_amount:
        goal.is_active = False
        goal.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(goal)
    db.commit()
    return {"detail": "Goal deleted"}