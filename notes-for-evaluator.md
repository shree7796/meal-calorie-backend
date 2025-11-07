# Notes for Evaluator — Meal Calorie Count API

This document summarises key design decisions, architecture, and testing notes for the Meal Calorie Count backend.  
The goal is transparency and clarity.

---

## High-Level Overview
This FastAPI application exposes:
1. **Authentication**
   - `/auth/register`
   - `/auth/login` (JWT-based)
2. **Calorie Estimation**
   - `/get-calories` → returns calories per serving & total calories
   - Powered by USDA FoodData Central API

Architecture emphasises OOP, modularity, and testability.

---

## Architecture Summary

### **1. Controllers**
- Located in `app/auth/auth_router.py` and `app/calories/controller.py`.
- Handle request validation, routing, and HTTP responses.

### **2. Services**
- `CalorieService`: calorie calculation logic, fuzzy matching, caching.
- `USDAClient`: handles external USDA API calls (async `httpx`).

### **3. Models**
- SQLModel used for DB entities (UserTable).
- Pydantic for request/response schemas.

### **4. Configuration**
- All configuration from `.env` using Pydantic Settings.
- `.env.example` provided.
- No secrets hard-coded.

### **5. Dependency Injection**
- `get_usda_client()` in `deps.py` uses `lru_cache()` for instance reuse.
- Makes testing & mocking easy.

---

## Key Feature Implementations

### **Fuzzy Matching**
- Uses `rapidfuzz.WRatio` to match misspellings such as:
  - “chiken breast” → “chicken breast”
  - “griled salmon” → “grilled salmon”
- `score_cutoff` prevents bad matches.

### **Caching**
- In-memory `TTLCache` (1-hour TTL) to reduce repeated USDA calls.
- Easily replaceable with Redis in production.

### **Rate Limiting**
- Implemented using `slowapi`.
- Configurable via `.env` (default: `15/minute`).

### **Error Handling**
- 400 → Bad input (invalid servings)
- 404 → Dish not found
- 401 → Invalid login
- 500 → Internal server error
- Clear and consistent error messages.

### **Authentication**
- Password hashing via `passlib[bcrypt]`
- JWT tokens via `python-jose`
- Token expiry configurable

---

## Assumptions & Heuristics
- USDA data varies; we extract `calories` from `foodNutrients`.
- If fuzzy match fails, system selects best USDA record available.
- Some items report calories per 100g; others per serving → unified into `calories_per_serving` for the response.
- In-memory cache suitable for single-worker environment (sufficient for assignment scope).

---

## Testing Notes
Tests cover:
- Registration & login
- Valid calorie-response flow
- Dish not found
- Invalid servings (0, negative, very large, fractional)
- Fuzzy misspellings (e.g., “chiken breast”)
- Cache check (repeated queries faster)

Tests use dependency overrides to mock USDAClient → no external calls.

Run:
```bash
pytest -q
