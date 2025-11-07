# 🍽️ Meal Calorie Count API

A lightweight, modular **FastAPI** backend that estimates calorie information for dishes using the **USDA FoodData Central API**.  
Designed to meet assignment requirements with clean OOP structure, environment-based configuration, authentication, caching, fuzzy matching, error handling, and rate limiting.

---

## 🚀 Quick Start

### 1. Create & activate virtual environment (Windows PowerShell & Ubuntu)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```Terminal
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install requirements
```
pip install -r requirements.txt
```

### 3. Sample .env
```
SECRET_KEY=replace_with_secure_random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

USDA_API_KEY=your_usda_api_key_here
USDA_BASE_URL=https://api.nal.usda.gov/fdc/v1/foods/search
PAGE_SIZE=10

DATABASE_URL=sqlite:///./dev.db
RATE_LIMIT=15/minute
```

### 4. Run the server
```
uvicorn app.main:app --reload

Open browser → http://127.0.0.1:8000

Docs → http://127.0.0.1:8000/docs
```

## 📁 Project Structure

meal-calorie-backend/
├─ app/
│  ├─ main.py
│  ├─ db.py
│  ├─ config.py
│  ├─ models.py
│  ├─ deps.py
│  ├─ middlewares.py
│  ├─ auth/
│  │  ├─ auth_router.py
│  │  ├─ auth_service.py
│  ├─ calories/
│  │  ├─ controller.py
│  │  ├─ service.py
│  │  ├─ usda_client.py
│  │  ├─ fuzzy.py
├─ tests/
│  ├─ test_auth.py
│  ├─ test_get_calories.py
├─ .env.example
├─ requirements.txt
├─ README.md

## 🔐 Authentication APIs

### Register
POST /auth/register

```
Request:
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "StrongPass123"
}

Response:
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

### Login
POST /auth/login

```
Request:
{
  "email": "john@example.com",
  "password": "StrongPass123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}

```

## 🥗 Calorie API

### Get Calories
POST /get-calories

```
Request:
{
  "dish_name": "grilled salmon",
  "servings": 2
}

Response:
{
  "dish_name": "grilled salmon",
  "servings": 2.0,
  "calories_per_serving": 232.5,
  "total_calories": 465.0,
  "source": "USDA FoodData Central"
}
```

## Error codes

| Status | Meaning                             |
| ------ | ----------------------------------- |
| 400    | Invalid input (e.g., servings <= 0) |
| 404    | Dish not found                      |
| 500    | Internal server error               |


## 🔍 Example Curl Commands

```
Register: 
curl -X POST http://127.0.0.1:8000/auth/register \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"12345"}'

```

```
Login
curl -X POST http://127.0.0.1:8000/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"john@example.com","password":"12345"}'
```

```
Get Calories
curl -X POST http://127.0.0.1:8000/get-calories \
-H "Content-Type: application/json" \
-d '{"dish_name":"chiken breast","servings":2}'
```
