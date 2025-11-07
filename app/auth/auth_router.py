from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..models import UserCreate, UserResponse, UserTable, Token
from ..db import get_session
from .auth_service import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    exists = session.exec(select(UserTable).where(UserTable.email == user_in.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = UserTable(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse.from_orm(user)

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(UserTable).where(UserTable.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
