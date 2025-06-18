#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных с тестовыми данными
"""

import os
import sys
from sqlalchemy.orm import Session

# Добавляем путь к приложению
sys.path.append(os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app.models import Base, Company, Bank, BankAccount
from app import crud, schemas

def init_db():
    """Инициализация базы данных с тестовыми данными"""
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные
        existing_companies = db.query(Company).count()
        if existing_companies > 0:
            print("База данных уже содержит данные. Пропускаем инициализацию.")
            return
        
        print("Создание тестовых данных...")
        
        # Создаем компании
        companies_data = [
            {
                "name": "ООО Рога и Копыта",
                "inn": "1234567890",
                "identifier": "COMP001"
            },
            {
                "name": "ИП Иванов И.И.",
                "inn": "123456789012",
                "identifier": "COMP002"
            },
            {
                "name": "АО Технологии Будущего",
                "inn": "9876543210",
                "identifier": "COMP003"
            }
        ]
        
        companies = []
        for company_data in companies_data:
            company = crud.create_company(db, schemas.CompanyCreate(**company_data))
            companies.append(company)
            print(f"Создана компания: {company.name}")
        
        # Создаем банки
        banks_data = [
            {
                "name": "Сбербанк России",
                "identifier": "SB001"
            },
            {
                "name": "ВТБ Банк",
                "identifier": "VT001"
            },
            {
                "name": "Альфа-Банк",
                "identifier": "AB001"
            }
        ]
        
        banks = []
        for bank_data in banks_data:
            bank = crud.create_bank(db, schemas.BankCreate(**bank_data))
            banks.append(bank)
            print(f"Создан банк: {bank.name}")
        
        # Создаем банковские счета
        accounts_data = [
            {
                "account_number": "12345678901234567890",
                "identifier": "ACC001",
                "company_id": companies[0].id,
                "bank_id": banks[0].id
            },
            {
                "account_number": "09876543210987654321",
                "identifier": "ACC002",
                "company_id": companies[0].id,
                "bank_id": banks[1].id
            },
            {
                "account_number": "11223344556677889900",
                "identifier": "ACC003",
                "company_id": companies[1].id,
                "bank_id": banks[0].id
            },
            {
                "account_number": "22334455667788990011",
                "identifier": "ACC004",
                "company_id": companies[2].id,
                "bank_id": banks[2].id
            }
        ]
        
        for account_data in accounts_data:
            account = crud.create_bank_account(db, schemas.BankAccountCreate(**account_data))
            print(f"Создан банковский счет: {account.account_number}")
        
        print("\n✅ База данных успешно инициализирована!")
        print(f"Создано: {len(companies)} компаний, {len(banks)} банков, {len(accounts_data)} банковских счетов")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 