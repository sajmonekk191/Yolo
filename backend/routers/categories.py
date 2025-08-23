from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db

router = APIRouter()

# Předdefinované kategorie s ikonami
CATEGORIES = [
    # Příjmy
    {"id": 1, "name": "Mzda", "type": "income", "icon": "Banknote", "color": "green"},
    {"id": 2, "name": "Freelance", "type": "income", "icon": "Briefcase", "color": "blue"},
    {"id": 3, "name": "Investice", "type": "income", "icon": "TrendingUp", "color": "purple"},
    {"id": 4, "name": "Dary", "type": "income", "icon": "Gift", "color": "pink"},
    {"id": 5, "name": "Ostatní příjmy", "type": "income", "icon": "Wallet", "color": "gray"},
    
    # Výdaje - Základní potřeby
    {"id": 6, "name": "Jídlo a potraviny", "type": "expense", "icon": "ShoppingCart", "color": "orange"},
    {"id": 7, "name": "Bydlení", "type": "expense", "icon": "Home", "color": "blue"},
    {"id": 8, "name": "Doprava", "type": "expense", "icon": "Car", "color": "indigo"},
    {"id": 9, "name": "Zdraví", "type": "expense", "icon": "Heart", "color": "red"},
    {"id": 10, "name": "Oblečení", "type": "expense", "icon": "Shirt", "color": "purple"},
    
    # Výdaje - Zábava a volný čas
    {"id": 11, "name": "Zábava", "type": "expense", "icon": "Music", "color": "pink"},
    {"id": 12, "name": "Restaurace", "type": "expense", "icon": "Utensils", "color": "yellow"},
    {"id": 13, "name": "Sport", "type": "expense", "icon": "Dumbbell", "color": "green"},
    {"id": 14, "name": "Cestování", "type": "expense", "icon": "Plane", "color": "cyan"},
    {"id": 15, "name": "Vzdělání", "type": "expense", "icon": "GraduationCap", "color": "blue"},
    
    # Výdaje - Služby a poplatky
    {"id": 16, "name": "Telefon a internet", "type": "expense", "icon": "Smartphone", "color": "gray"},
    {"id": 17, "name": "Pojištění", "type": "expense", "icon": "Shield", "color": "green"},
    {"id": 18, "name": "Energie", "type": "expense", "icon": "Zap", "color": "yellow"},
    {"id": 19, "name": "Předplatné", "type": "expense", "icon": "CreditCard", "color": "purple"},
    
    # Ostatní
    {"id": 20, "name": "Ostatní výdaje", "type": "expense", "icon": "MoreHorizontal", "color": "gray"},
]

@router.get("/")
def get_categories(type: str = None):
    """Získat seznam kategorií, volitelně filtrované podle typu"""
    if type:
        return [cat for cat in CATEGORIES if cat["type"] == type]
    return CATEGORIES

@router.get("/{category_id}")
def get_category(category_id: int):
    """Získat konkrétní kategorii podle ID"""
    category = next((cat for cat in CATEGORIES if cat["id"] == category_id), None)
    if not category:
        raise HTTPException(status_code=404, detail="Kategorie nenalezena")
    return category