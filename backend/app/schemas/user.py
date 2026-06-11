from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    specialty: str | None = None
    level: str | None = None


class UserUpdate(BaseModel):
    specialty: str | None = None
    level: str | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    specialty: str | None
    level: str | None
    is_verified: bool
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }