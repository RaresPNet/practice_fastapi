from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_db, get_current_active_superuser, get_current_active_user

router = APIRouter()

@router.post(
    "/",
    status_code=201,
    response_model=schemas.Company,
    dependencies=[Depends(get_current_active_superuser)]
)
def create_company(
    company_in: schemas.CompanyCreate, 
    db: Session = Depends(get_db)
):
    company = crud.company.get_by_name(db, name=company_in.name)
    if company:
        raise HTTPException(
            status_code=400,
            detail="Company with the same name already exists.",
        )
    return crud.company.create(db, obj_in=company_in)

@router.get(
    "/", 
    response_model=List[schemas.Company]
)
def read_companies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.is_superuser:
        return crud.company.get_multi(db, skip=skip, limit=limit)
    
    return crud.company.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )

@router.get(
    "/{company_id}",
    response_model=schemas.CompanyWithEmployees,
)
def read_company_by_id(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code = 404,
            detail="Company does not exist."
        )
    if not (current_user.is_superuser or company.owner_id == current_user.id):
        raise HTTPException(
            status_code = 403,
            detail = "You do not have permission to access this company"
        )
    
    return company


@router.patch(
    "/{company_id}/verify",
    response_model=schemas.Company
)
def verify_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_superuser)
):
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code = 404,
            detail = "Company does not exist"
        )
    
    return crud.company.update(db, db_obj=company, obj_in={"is_verified": True})