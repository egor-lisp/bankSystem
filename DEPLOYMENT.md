# Инструкции по развертыванию

## Быстрый старт с Docker

### 1. Запуск с Docker Compose

```bash
# Клонирование репозитория
git clone <your-repo-url>
cd bankSystem

# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f app
```

### 2. Инициализация базы данных

```bash
# Запуск скрипта инициализации
docker-compose exec app python init_db.py
```

### 3. Проверка работы

```bash
# Тестирование API
python test_api.py

# Или вручную
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/companies/
```

## Локальная разработка

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv venv

# Активация окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Запуск PostgreSQL через Docker
docker-compose up -d postgres

# Ожидание запуска базы данных
sleep 10

# Инициализация базы данных
python init_db.py
```

### 3. Запуск приложения

```bash
# Запуск через uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Или через скрипт
python run.py
```

## Миграции базы данных

### Создание миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Просмотр истории
alembic history
```

## Production развертывание

### 1. Создание production docker-compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: banksystem
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - bank_network

  app:
    build: .
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/banksystem
    depends_on:
      - postgres
    networks:
      - bank_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  bank_network:
    driver: bridge
```

### 2. Переменные окружения

Создайте файл `.env`:

```env
DB_USER=postgres
DB_PASSWORD=secure_password
DATABASE_URL=postgresql://postgres:secure_password@postgres:5432/banksystem
```

### 3. Запуск в production

```bash
# Запуск production версии
docker-compose -f docker-compose.prod.yml up -d

# Применение миграций
docker-compose -f docker-compose.prod.yml exec app alembic upgrade head

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

## Мониторинг и логи

### Просмотр логов

```bash
# Логи приложения
docker-compose logs -f app

# Логи базы данных
docker-compose logs -f postgres

# Все логи
docker-compose logs -f
```

### Health Check

```bash
# Проверка состояния API
curl http://localhost:8000/health

# Ожидаемый ответ:
# {"status": "healthy", "message": "API работает корректно"}
```

## Безопасность

### Рекомендации для production

1. **Изменение паролей по умолчанию**
2. **Настройка SSL/TLS**
3. **Ограничение доступа к базе данных**
4. **Настройка firewall**
5. **Регулярное резервное копирование**

### Пример настройки nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Частые проблемы

1. **Ошибка подключения к базе данных**
   ```bash
   # Проверьте статус PostgreSQL
   docker-compose ps postgres
   
   # Перезапустите сервис
   docker-compose restart postgres
   ```

2. **Ошибки миграций**
   ```bash
   # Сброс миграций
   docker-compose exec app alembic downgrade base
   docker-compose exec app alembic upgrade head
   ```

3. **Проблемы с портами**
   ```bash
   # Проверьте занятые порты
   netstat -tulpn | grep :8000
   
   # Измените порт в docker-compose.yml
   ```

### Логи ошибок

```bash
# Подробные логи приложения
docker-compose logs app

# Логи с временными метками
docker-compose logs -t app
``` 