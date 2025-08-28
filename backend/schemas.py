from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import TransactionType, ExpenseCategory, Frequency

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Transaction schemas
class TransactionBase(BaseModel):
    type: TransactionType
    category_id: Optional[int] = None
    amount: float
    description: str
    date: Optional[datetime] = None
    is_recurring: bool = False
    frequency: Optional[Frequency] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Goal schemas
class GoalBase(BaseModel):
    name: str
    target_amount: float
    deadline: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    current_amount: Optional[float] = None
    is_active: Optional[bool] = None

class Goal(GoalBase):
    id: int
    user_id: int
    current_amount: float
    is_active: bool
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Budget schemas
class BudgetBase(BaseModel):
    category_id: int
    amount: float
    month: int
    year: int
    is_active: bool = True

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int
    spent: float = 0
    created_at: datetime
    category: Optional[str] = None
    
    class Config:
        from_attributes = True

# Dashboard schemas
class DashboardStats(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    monthly_income: float
    monthly_expenses: float
    active_goals: int
    total_goals_progress: float
    budget_utilization: float