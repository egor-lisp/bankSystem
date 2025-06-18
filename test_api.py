#!/usr/bin/env python3
"""
Простой тест для проверки работы API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Тест health check"""
    print("🔍 Тестирование health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check работает")
            return True
        else:
            print(f"❌ Health check не работает: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return False

def test_create_company():
    """Тест создания компании"""
    print("\n🔍 Тестирование создания компании...")
    
    company_data = {
        "name": "Тестовая Компания",
        "inn": "1111111111",
        "identifier": "TEST001"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/companies/",
            json=company_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            company = response.json()
            print(f"✅ Компания создана: {company['name']} (ID: {company['id']})")
            return company['id']
        else:
            print(f"❌ Ошибка создания компании: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_create_bank():
    """Тест создания банка"""
    print("\n🔍 Тестирование создания банка...")
    
    bank_data = {
        "name": "Тестовый Банк",
        "identifier": "TESTBANK001"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/banks/",
            json=bank_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            bank = response.json()
            print(f"✅ Банк создан: {bank['name']} (ID: {bank['id']})")
            return bank['id']
        else:
            print(f"❌ Ошибка создания банка: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_create_account(company_id, bank_id):
    """Тест создания банковского счета"""
    print("\n🔍 Тестирование создания банковского счета...")
    
    account_data = {
        "account_number": "12345678901234567890",
        "identifier": "TESTACC001",
        "company_id": company_id,
        "bank_id": bank_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/accounts/",
            json=account_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            account = response.json()
            print(f"✅ Банковский счет создан: {account['account_number']} (ID: {account['id']})")
            return account['id']
        else:
            print(f"❌ Ошибка создания счета: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_get_companies():
    """Тест получения списка компаний"""
    print("\n🔍 Тестирование получения списка компаний...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/companies/")
        
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ Получено компаний: {len(companies)}")
            for company in companies:
                print(f"  - {company['name']} (ИНН: {company['inn']})")
            return True
        else:
            print(f"❌ Ошибка получения компаний: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_get_banks():
    """Тест получения списка банков"""
    print("\n🔍 Тестирование получения списка банков...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/banks/")
        
        if response.status_code == 200:
            banks = response.json()
            print(f"✅ Получено банков: {len(banks)}")
            for bank in banks:
                print(f"  - {bank['name']} (ID: {bank['identifier']})")
            return True
        else:
            print(f"❌ Ошибка получения банков: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_get_accounts():
    """Тест получения списка банковских счетов"""
    print("\n🔍 Тестирование получения списка банковских счетов...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/accounts/")
        
        if response.status_code == 200:
            accounts = response.json()
            print(f"✅ Получено банковских счетов: {len(accounts)}")
            for account in accounts:
                print(f"  - Счет: {account['account_number']} (ID: {account['identifier']})")
            return True
        else:
            print(f"❌ Ошибка получения счетов: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов API...")
    print("=" * 50)
    
    # Проверяем доступность API
    if not test_health():
        return
    
    # Тестируем создание сущностей
    company_id = test_create_company()
    bank_id = test_create_bank()
    
    if company_id and bank_id:
        account_id = test_create_account(company_id, bank_id)
    
    # Тестируем получение данных
    test_get_companies()
    test_get_banks()
    test_get_accounts()
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print(f"📖 Документация API: {BASE_URL}/docs")

if __name__ == "__main__":
    main() 