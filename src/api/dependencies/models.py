from pydantic import BaseModel, EmailStr


class AuthenticatedUser(BaseModel):
    id : int
    email : EmailStr