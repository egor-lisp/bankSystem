#!/usr/bin/env python3
"""
Скрипт для запуска приложения
"""

import uvicorn
import os

if __name__ == "__main__":
    # Получаем порт из переменной окружения или используем 8000
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Запуск Bank System API на порту {port}...")
    print(f"📖 Документация будет доступна по адресу: http://localhost:{port}/docs")
    print(f"🔍 Health check: http://localhost:{port}/health")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=port,
        reload=True,
        log_level="info"
    ) 