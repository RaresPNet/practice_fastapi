from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Company]:
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Company]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(
        self, db: Session, *, db_obj: Company, obj_in: Union[CompanyUpdate, Dict[str, Any]]
    ) -> Company:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def is_verified(self, company: Company) -> bool:
        return company.is_verified
    
company = CRUDCompany(Company)