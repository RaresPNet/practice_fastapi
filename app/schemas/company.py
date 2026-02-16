from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import date

from app.schemas.user import User

class CompanyBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    is_verified: bool = False
    website_url: Optional[str] = None
    tax_id: Optional[str] = None

# props to receive on company creation
class CompanyCreate(CompanyBase):
    owner_id: int
    pass

class CompanyUpdate(CompanyBase):
    # We make name optional here because it was required in CompanyBase
    name: Optional[str] = None
    pass

class Company(CompanyBase):
    id: int
    created_at: date

    class Config:
        orm_mode = True

class CompanyWithEmployees(Company):
    employees: List[User] = []