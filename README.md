# 🚀 Yolo Finance - Kompletní finanční aplikace

## ✅ Plně funkční aplikace s:
- Vue 3 + Vite + Tailwind CSS (frontend)
- FastAPI + SQLite (backend)
- JWT autentizace
- Kompletní CRUD operace
- Responzivní design

## 📦 Instalace a spuštění

### Backend (Port 8000)
```bash
cd backend
source venv/bin/activate  # Na Mac/Linux
# nebo
venv\Scripts\activate  # Na Windows

# Instalace závislostí (pokud je potřeba)
pip install -r requirements.txt

# Spuštění serveru
python3 main.py
```

### Frontend (Port 5173)
```bash
cd frontend
npm install  # Instalace závislostí
npm run dev  # Spuštění vývojového serveru
```

## 🔑 Přihlašovací údaje

### Demo účet
- **Email:** demo@yolo-finance.cz
- **Heslo:** demo123

### Testovací účet
- **Email:** test@test.cz
- **Heslo:** test123

## 🛠 API Endpointy

### Autentizace
- `POST /api/auth/login` - Přihlášení (FormData: username, password)
- `POST /api/auth/register` - Registrace (JSON: email, username, password)

### Uživatel
- `GET /api/users/me` - Získat aktuálního uživatele

### Transakce
- `GET /api/transactions` - Seznam transakcí
- `POST /api/transactions` - Vytvořit transakci
- `PUT /api/transactions/{id}` - Upravit transakci
- `DELETE /api/transactions/{id}` - Smazat transakci

### Cíle
- `GET /api/goals` - Seznam cílů
- `POST /api/goals` - Vytvořit cíl
- `PUT /api/goals/{id}` - Upravit cíl
- `POST /api/goals/{id}/contribute` - Přidat příspěvek k cíli
- `DELETE /api/goals/{id}` - Smazat cíl

### Rozpočty
- `GET /api/budgets` - Seznam rozpočtů
- `POST /api/budgets` - Vytvořit rozpočet
- `PUT /api/budgets/{id}` - Upravit rozpočet
- `DELETE /api/budgets/{id}` - Smazat rozpočet

### Dashboard
- `GET /api/dashboard/stats` - Statistiky
- `GET /api/dashboard/recent-transactions` - Poslední transakce
- `GET /api/dashboard/category-breakdown` - Rozdělení podle kategorií

## 📁 Struktura projektu

```
yolo-finance/
├── backend/
│   ├── venv/              # Python virtual environment
│   ├── routers/           # API routery
│   ├── main.py           # Hlavní FastAPI aplikace
│   ├── models.py         # SQLAlchemy modely
│   ├── schemas.py        # Pydantic schémata
│   ├── auth.py           # Autentizace
│   ├── database.py       # Databázové připojení
│   ├── init_db.py        # Inicializace databáze
│   └── yolo_finance.db   # SQLite databáze
│
└── frontend/
    ├── src/
    │   ├── api/          # API client
    │   ├── components/   # Vue komponenty
    │   ├── router/       # Vue Router
    │   ├── stores/       # Pinia stores
    │   ├── views/        # Stránky aplikace
    │   ├── App.vue       # Hlavní komponenta
    │   └── main.js       # Vstupní bod
    ├── package.json      # NPM závislosti
    └── vite.config.js    # Vite konfigurace
```

## ⚠️ Důležité poznámky

1. **CORS** - Backend má povolené všechny originy pro vývoj. Pro produkci změňte v `main.py`
2. **Secret Key** - Změňte SECRET_KEY v `backend/auth.py` pro produkci
3. **Databáze** - SQLite je vhodná pro vývoj. Pro produkci použijte PostgreSQL
4. **HTTPS** - Pro produkci používejte HTTPS

## 🔄 Reset databáze

Pokud potřebujete resetovat databázi s testovacími daty:
```bash
cd backend
source venv/bin/activate
python3 init_db.py
```

## 🎯 Funkce aplikace

- ✅ Registrace a přihlášení uživatelů
- ✅ Dashboard s přehledem financí
- ✅ Správa příjmů a výdajů  
- ✅ Finanční cíle s progress bary
- ✅ Měsíční rozpočty podle kategorií
- ✅ Kompletní CRUD operace
- ✅ Responzivní design pro mobily, tablety a desktop
- ✅ České lokalizace
- ✅ **NOVĚ: Interaktivní grafy a vizualizace (Chart.js)**
- ✅ **NOVĚ: Měsíční trendy příjmů a výdajů**
- ✅ **NOVĚ: Rozložení výdajů podle kategorií**
- ✅ **NOVĚ: Statistické karty s gradientním designem**
- ✅ **NOVĚ: Pokročilé API endpointy pro analýzu dat**

## 🚨 Řešení problémů

### Frontend hlásí chybu s PostCSS/Tailwind
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend hlásí chybu s email-validator
```bash
cd backend
source venv/bin/activate
pip install email-validator
```

### Port je obsazený
- Frontend běží standardně na portu 5173
- Pokud je obsazený, Vite automaticky použije 5174
- Backend běží na portu 8000

## 📞 Kontakt

Projekt vytvořen pro Yolo Finance
Verze: 1.0.0
Datum: 2025-08-22