# Bank System API

API для управления банковскими счетами компаний, построенный на FastAPI с использованием PostgreSQL и SQLAlchemy.

## Описание

Система предоставляет функционал для работы с:
- **Компаниями** - создание, редактирование, удаление компаний
- **Банками** - управление банковскими учреждениями  
- **Банковскими счетами** - создание и управление счетами компаний в банках

## Технологии

- **Python 3.11**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - база данных
- **Pydantic** - валидация данных
- **Alembic** - миграции базы данных
- **Docker & Docker Compose** - контейнеризация

## Структура проекта

```
bankSystem/
├── app/
│   ├── __init__.py
│   ├── main.py              # Главный файл приложения
│   ├── database.py          # Конфигурация базы данных
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── crud.py              # CRUD операции
│   └── api/
│       ├── __init__.py
│       ├── company.py       # API для компаний
│       ├── bank.py          # API для банков
│       └── account.py       # API для счетов
├── alembic/                 # Миграции базы данных
├── requirements.txt         # Зависимости Python
├── docker-compose.yml       # Docker Compose конфигурация
├── Dockerfile              # Docker образ
└── README.md               # Документация
```

## Быстрый старт

### 1. Клонирование репозитория
```bash
git clone <your-repo-url>
cd bankSystem
```

### 2. Запуск с Docker Compose
```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f app
```

### 3. Доступ к API
- **API документация**: http://localhost:8000/docs
- **ReDoc документация**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## API Endpoints

### Компании (`/api/v1/companies`)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/` | Создать компанию |
| GET | `/` | Получить список компаний |
| GET | `/{company_id}` | Получить компанию с счетами |
| PUT | `/{company_id}` | Обновить компанию |
| DELETE | `/{company_id}` | Удалить компанию |

### Банки (`/api/v1/banks`)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/` | Создать банк |
| GET | `/` | Получить список банков |
| GET | `/{bank_id}` | Получить банк со счетами |
| PUT | `/{bank_id}` | Обновить банк |
| DELETE | `/{bank_id}` | Удалить банк |

### Банковские счета (`/api/v1/accounts`)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/` | Создать банковский счет |
| GET | `/` | Получить список счетов |
| GET | `/{account_id}` | Получить счет с данными |
| PUT | `/{account_id}` | Обновить счет |
| DELETE | `/{account_id}` | Удалить счет |

## Модели данных

### Компания
```json
{
  "id": 1,
  "name": "ООО Рога и Копыта",
  "inn": "1234567890",
  "identifier": "COMP001",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Банк
```json
{
  "id": 1,
  "name": "Сбербанк России",
  "identifier": "SB001",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Банковский счет
```json
{
  "id": 1,
  "account_number": "12345678901234567890",
  "identifier": "ACC001",
  "company_id": 1,
  "bank_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## Валидация данных

### ИНН (Идентификационный номер налогоплательщика)
- Должен содержать 10 или 12 цифр
- Уникален в системе

### Номер банковского счета
- Должен содержать ровно 20 цифр
- Уникален в пределах одного банка

### Идентификаторы
- Должны быть уникальными в пределах своей сущности
- Минимальная длина: 1 символ
- Максимальная длина: 50 символов

## Примеры использования

### Создание компании
```bash
curl -X POST "http://localhost:8000/api/v1/companies/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ООО Рога и Копыта",
    "inn": "1234567890",
    "identifier": "COMP001"
  }'
```

### Создание банка
```bash
curl -X POST "http://localhost:8000/api/v1/banks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Сбербанк России",
    "identifier": "SB001"
  }'
```

### Создание банковского счета
```bash
curl -X POST "http://localhost:8000/api/v1/accounts/" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "12345678901234567890",
    "identifier": "ACC001",
    "company_id": 1,
    "bank_id": 1
  }'
```

## Разработка

### Локальная разработка

1. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

2. **Настройка базы данных**
```bash
# Запуск PostgreSQL
docker-compose up -d postgres

# Создание миграций
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
alembic upgrade head
```

3. **Запуск приложения**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Миграции базы данных

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Description of changes"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Просмотр истории миграций
alembic history
```

## Тестирование

### Запуск тестов
```bash
# Установка тестовых зависимостей
pip install pytest pytest-asyncio httpx

# Запуск тестов
pytest
```

## Развертывание

### Production
```bash
# Сборка и запуск
docker-compose -f docker-compose.prod.yml up -d

# Применение миграций
docker-compose exec app alembic upgrade head
```

## Мониторинг

### Health Check
```bash
curl http://localhost:8000/health
```

### Логи
```bash
# Просмотр логов приложения
docker-compose logs -f app

# Просмотр логов базы данных
docker-compose logs -f postgres
```

## Безопасность

- Все входные данные валидируются через Pydantic
- SQL-инъекции предотвращаются через SQLAlchemy ORM
- CORS настроен для разрешения кросс-доменных запросов
- Обработка ошибок с информативными сообщениями

## Лицензия

MIT License

## Поддержка

Для вопросов и предложений создавайте Issues в репозитории. 