from pydantic import BaseModel, EmailStr

class WelcomeEmailMessage(BaseModel):
    user_id: int
    email: EmailStr
    name: str | None = None