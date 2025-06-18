from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(prefix="/banks", tags=["banks"])

@router.post("/", response_model=schemas.Bank, status_code=201)
def create_bank(bank: schemas.BankCreate, db: Session = Depends(database.get_db)):
    """
    Создать новый банк
    """
    return crud.create_bank(db=db, bank=bank)

@router.get("/", response_model=List[schemas.Bank])
def read_banks(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    db: Session = Depends(database.get_db)
):
    """
    Получить список всех банков
    """
    banks = crud.get_banks(db, skip=skip, limit=limit)
    return banks

@router.get("/{bank_id}", response_model=schemas.BankWithAccounts)
def read_bank(bank_id: int, db: Session = Depends(database.get_db)):
    """
    Получить банк по ID с привязанными банковскими счетами
    """
    bank = crud.get_bank_with_accounts(db, bank_id=bank_id)
    if bank is None:
        raise HTTPException(status_code=404, detail="Банк не найден")
    return bank

@router.put("/{bank_id}", response_model=schemas.Bank)
def update_bank(
    bank_id: int, 
    bank: schemas.BankUpdate, 
    db: Session = Depends(database.get_db)
):
    """
    Обновить данные банка
    """
    db_bank = crud.update_bank(db, bank_id=bank_id, bank=bank)
    if db_bank is None:
        raise HTTPException(status_code=404, detail="Банк не найден")
    return db_bank

@router.delete("/{bank_id}", status_code=204)
def delete_bank(bank_id: int, db: Session = Depends(database.get_db)):
    """
    Удалить банк
    """
    success = crud.delete_bank(db, bank_id=bank_id)
    if not success:
        raise HTTPException(status_code=404, detail="Банк не найден")
    return {"message": "Банк успешно удален"} 