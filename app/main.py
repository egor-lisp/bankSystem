from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .api import company, bank, account

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Bank System API",
    description="API для управления банковскими счетами компаний",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(company.router, prefix="/api/v1")
app.include_router(bank.router, prefix="/api/v1")
app.include_router(account.router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Корневой эндпоинт с информацией о API
    """
    return {
        "message": "Bank System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "companies": "/api/v1/companies",
            "banks": "/api/v1/banks", 
            "accounts": "/api/v1/accounts"
        }
    }

@app.get("/health")
async def health_check():
    """
    Проверка состояния API
    """
    return {"status": "healthy", "message": "API работает корректно"}

# Обработчик ошибок
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Ресурс не найден", "detail": str(exc)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Внутренняя ошибка сервера", "detail": str(exc)} 