from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr 
    password: str 


class TokenResponse(BaseModel):
    access_token: str
    # token_type: str = "bearer"