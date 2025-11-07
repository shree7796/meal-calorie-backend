import uvicorn
from fastapi import FastAPI
from .db import init_db
from .config import settings
from .auth.auth_router import router as auth_router
from .calories.controller import router as calories_router
from .middlewares import init_middlewares
from .deps import get_usda_client

app = FastAPI(title="Meal Calorie Count")

init_middlewares(app)
app.include_router(auth_router)
app.include_router(calories_router)

@app.on_event("startup")
def on_startup():
    init_db()

# optional root
@app.get("/")
def root():
    return {"message": "Meal Calorie Count API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
