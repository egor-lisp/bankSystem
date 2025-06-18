from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from . import models, schemas
from fastapi import HTTPException

# CRUD операции для компаний
def create_company(db: Session, company: schemas.CompanyCreate) -> models.Company:
    try:
        db_company = models.Company(**company.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Компания с таким ИНН или идентификатором уже существует")

def get_company(db: Session, company_id: int) -> Optional[models.Company]:
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Company]:
    return db.query(models.Company).offset(skip).limit(limit).all()

def update_company(db: Session, company_id: int, company: schemas.CompanyUpdate) -> Optional[models.Company]:
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    
    try:
        update_data = company.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        
        db.commit()
        db.refresh(db_company)
        return db_company
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Компания с таким ИНН или идентификатором уже существует")

def delete_company(db: Session, company_id: int) -> bool:
    db_company = get_company(db, company_id)
    if not db_company:
        return False
    
    db.delete(db_company)
    db.commit()
    return True

# CRUD операции для банков
def create_bank(db: Session, bank: schemas.BankCreate) -> models.Bank:
    try:
        db_bank = models.Bank(**bank.dict())
        db.add(db_bank)
        db.commit()
        db.refresh(db_bank)
        return db_bank
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Банк с таким идентификатором уже существует")

def get_bank(db: Session, bank_id: int) -> Optional[models.Bank]:
    return db.query(models.Bank).filter(models.Bank.id == bank_id).first()

def get_banks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Bank]:
    return db.query(models.Bank).offset(skip).limit(limit).all()

def update_bank(db: Session, bank_id: int, bank: schemas.BankUpdate) -> Optional[models.Bank]:
    db_bank = get_bank(db, bank_id)
    if not db_bank:
        return None
    
    try:
        update_data = bank.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bank, field, value)
        
        db.commit()
        db.refresh(db_bank)
        return db_bank
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Банк с таким идентификатором уже существует")

def delete_bank(db: Session, bank_id: int) -> bool:
    db_bank = get_bank(db, bank_id)
    if not db_bank:
        return False
    
    db.delete(db_bank)
    db.commit()
    return True

# CRUD операции для банковских счетов
def create_bank_account(db: Session, account: schemas.BankAccountCreate) -> models.BankAccount:
    # Проверяем существование компании и банка
    company = get_company(db, account.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    
    bank = get_bank(db, account.bank_id)
    if not bank:
        raise HTTPException(status_code=404, detail="Банк не найден")
    
    try:
        db_account = models.BankAccount(**account.dict())
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Банковский счет с таким номером уже существует в данном банке или идентификатор уже используется")

def get_bank_account(db: Session, account_id: int) -> Optional[models.BankAccount]:
    return db.query(models.BankAccount).filter(models.BankAccount.id == account_id).first()

def get_bank_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[models.BankAccount]:
    return db.query(models.BankAccount).offset(skip).limit(limit).all()

def update_bank_account(db: Session, account_id: int, account: schemas.BankAccountUpdate) -> Optional[models.BankAccount]:
    db_account = get_bank_account(db, account_id)
    if not db_account:
        return None
    
    # Проверяем существование компании и банка если они обновляются
    update_data = account.dict(exclude_unset=True)
    
    if 'company_id' in update_data:
        company = get_company(db, update_data['company_id'])
        if not company:
            raise HTTPException(status_code=404, detail="Компания не найдена")
    
    if 'bank_id' in update_data:
        bank = get_bank(db, update_data['bank_id'])
        if not bank:
            raise HTTPException(status_code=404, detail="Банк не найден")
    
    try:
        for field, value in update_data.items():
            setattr(db_account, field, value)
        
        db.commit()
        db.refresh(db_account)
        return db_account
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Банковский счет с таким номером уже существует в данном банке или идентификатор уже используется")

def delete_bank_account(db: Session, account_id: int) -> bool:
    db_account = get_bank_account(db, account_id)
    if not db_account:
        return False
    
    db.delete(db_account)
    db.commit()
    return True

# Дополнительные операции для получения связанных данных
def get_company_with_accounts(db: Session, company_id: int) -> Optional[models.Company]:
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_bank_with_accounts(db: Session, bank_id: int) -> Optional[models.Bank]:
    return db.query(models.Bank).filter(models.Bank.id == bank_id).first()

def get_bank_account_with_relations(db: Session, account_id: int) -> Optional[models.BankAccount]:
    return db.query(models.BankAccount).filter(models.BankAccount.id == account_id).first() 