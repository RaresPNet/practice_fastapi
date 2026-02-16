from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import date

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

class Company(CompanyBase):
    id: int
    created_at: date

    class Config:
        orm_mode = True

class CompanyWithEmployees(Company):
    emplyee_ids: List[int] = []