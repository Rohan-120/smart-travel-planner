"""
Authentication & RBAC
Simple session-based login using PostgreSQL user records.
Roles: admin, travel_agent, user
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    from database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return session token."""
    # TODO: verify password hash, create session
    raise NotImplementedError("Login is not yet implemented")


@router.post("/logout")
def logout():
    """Invalidate current session."""
    # TODO: clear session
    raise NotImplementedError("Logout is not yet implemented")
