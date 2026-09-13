import random
import string
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.database.connection import SessionLocal
from app.database.models import User
from app.utils.security import hash_password
from app.utils.email_utils import send_verification_email

router = APIRouter(prefix="/api/users", tags=["Users"])

CODE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class VerifyRequest(BaseModel):
    email: EmailStr
    code: str


class UpdateNameRequest(BaseModel):
    name: str


@router.post("/register")
def register(payload: RegisterRequest):
    session = SessionLocal()
    existing = session.query(User).filter(User.email == payload.email).first()
    if existing:
        session.close()
        raise HTTPException(status_code=400, detail="You already have a code, you can use that one.")

    code = "".join(random.choices(CODE_CHARS, k=8))
    user = User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        code=code,
        isactive=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()

    # send_verification_email(payload.email, code)

    # return {"message": "User registered. Check your email for the verification code.", "user_id": user.id}
    return {"message": "User registered. Check your email for the verification code.", "user_id": user.id, "code": code}

@router.post("/verify")
def verify(payload: VerifyRequest):
    session = SessionLocal()
    user = session.query(User).filter(User.email == payload.email).first()

    if not user or user.code != payload.code:
        session.close()
        raise HTTPException(status_code=400, detail="Invalid verification code.")

    user.isactive = True
    user.updatedat = datetime.utcnow()
    session.commit()
    session.close()

    return {"message": "Account verified successfully."}


@router.get("/{user_id}")
def get_user(user_id: int):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "isactive": user.isactive,
        "createdat": user.createdat,
        "updatedat": user.updatedat,
    }


@router.put("/{user_id}")
def update_user(user_id: int, payload: UpdateNameRequest):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        session.close()
        raise HTTPException(status_code=404, detail="User not found.")

    user.name = payload.name
    user.updatedat = datetime.utcnow()
    session.commit()
    session.close()

    return {"message": "Name updated successfully."}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        session.close()
        raise HTTPException(status_code=404, detail="User not found.")

    session.delete(user)
    session.commit()
    session.close()

    return {"message": "User deleted successfully."}