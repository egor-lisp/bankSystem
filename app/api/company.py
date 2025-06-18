from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=schemas.Company, status_code=201)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(database.get_db)):
    """
    Создать новую компанию
    """
    return crud.create_company(db=db, company=company)

@router.get("/", response_model=List[schemas.Company])
def read_companies(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    db: Session = Depends(database.get_db)
):
    """
    Получить список всех компаний
    """
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

@router.get("/{company_id}", response_model=schemas.CompanyWithAccounts)
def read_company(company_id: int, db: Session = Depends(database.get_db)):
    """
    Получить компанию по ID с привязанными банковскими счетами
    """
    company = crud.get_company_with_accounts(db, company_id=company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    return company

@router.put("/{company_id}", response_model=schemas.Company)
def update_company(
    company_id: int, 
    company: schemas.CompanyUpdate, 
    db: Session = Depends(database.get_db)
):
    """
    Обновить данные компании
    """
    db_company = crud.update_company(db, company_id=company_id, company=company)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    return db_company

@router.delete("/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(database.get_db)):
    """
    Удалить компанию
    """
    success = crud.delete_company(db, company_id=company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    return {"message": "Компания успешно удалена"} 