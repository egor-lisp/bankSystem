from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=schemas.BankAccount, status_code=201)
def create_bank_account(account: schemas.BankAccountCreate, db: Session = Depends(database.get_db)):
    """
    Создать новый банковский счет
    """
    return crud.create_bank_account(db=db, account=account)

@router.get("/", response_model=List[schemas.BankAccountWithRelations])
def read_bank_accounts(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    db: Session = Depends(database.get_db)
):
    """
    Получить список всех банковских счетов с информацией о компаниях и банках
    """
    accounts = crud.get_bank_accounts(db, skip=skip, limit=limit)
    return accounts

@router.get("/{account_id}", response_model=schemas.BankAccountWithRelations)
def read_bank_account(account_id: int, db: Session = Depends(database.get_db)):
    """
    Получить банковский счет по ID с информацией о компании и банке
    """
    account = crud.get_bank_account_with_relations(db, account_id=account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Банковский счет не найден")
    return account

@router.put("/{account_id}", response_model=schemas.BankAccount)
def update_bank_account(
    account_id: int, 
    account: schemas.BankAccountUpdate, 
    db: Session = Depends(database.get_db)
):
    """
    Обновить данные банковского счета
    """
    db_account = crud.update_bank_account(db, account_id=account_id, account=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Банковский счет не найден")
    return db_account

@router.delete("/{account_id}", status_code=204)
def delete_bank_account(account_id: int, db: Session = Depends(database.get_db)):
    """
    Удалить банковский счет
    """
    success = crud.delete_bank_account(db, account_id=account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Банковский счет не найден")
    return {"message": "Банковский счет успешно удален"} 