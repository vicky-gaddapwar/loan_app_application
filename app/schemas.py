from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class LoanCreate(BaseModel):
    loan_amount: float
    loan_purpose: str
    duration: int
    contact_details: str

class LoanStatus(BaseModel):
    application_id: int
    status: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
