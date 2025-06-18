from pydantic import BaseModel, validator, constr
from typing import List, Optional
from datetime import datetime
import re

# Базовые схемы для компаний
class CompanyBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    inn: constr(min_length=10, max_length=12)
    identifier: constr(min_length=1, max_length=50)
    
    @validator('inn')
    def validate_inn(cls, v):
        if not re.match(r'^\d{10}(\d{2})?$', v):
            raise ValueError('ИНН должен содержать 10 или 12 цифр')
        return v

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)] = None
    inn: Optional[constr(min_length=10, max_length=12)] = None
    identifier: Optional[constr(min_length=1, max_length=50)] = None
    
    @validator('inn')
    def validate_inn(cls, v):
        if v is not None and not re.match(r'^\d{10}(\d{2})?$', v):
            raise ValueError('ИНН должен содержать 10 или 12 цифр')
        return v

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Базовые схемы для банков
class BankBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    identifier: constr(min_length=1, max_length=50)

class BankCreate(BankBase):
    pass

class BankUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)] = None
    identifier: Optional[constr(min_length=1, max_length=50)] = None

class Bank(BankBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Базовые схемы для банковских счетов
class BankAccountBase(BaseModel):
    account_number: constr(min_length=1, max_length=20)
    identifier: constr(min_length=1, max_length=50)
    company_id: int
    bank_id: int
    
    @validator('account_number')
    def validate_account_number(cls, v):
        if not re.match(r'^\d{20}$', v):
            raise ValueError('Номер счета должен содержать 20 цифр')
        return v

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BaseModel):
    account_number: Optional[constr(min_length=1, max_length=20)] = None
    identifier: Optional[constr(min_length=1, max_length=50)] = None
    company_id: Optional[int] = None
    bank_id: Optional[int] = None
    
    @validator('account_number')
    def validate_account_number(cls, v):
        if v is not None and not re.match(r'^\d{20}$', v):
            raise ValueError('Номер счета должен содержать 20 цифр')
        return v

class BankAccount(BankAccountBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Расширенные схемы с связанными данными
class BankAccountWithRelations(BankAccount):
    company: Company
    bank: Bank

class CompanyWithAccounts(Company):
    accounts: List[BankAccountWithRelations] = []

class BankWithAccounts(Bank):
    accounts: List[BankAccountWithRelations] = [] 