from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import User
import time
from starlette.middleware.base import BaseHTTPMiddleware

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])

# Время запуска сервиса (при старте приложения)
START_TIME = time.time()

# Метрики для измерения времени ответа
request_count = 0
total_response_time = 0

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global request_count, total_response_time
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Обновляем метрики (исключаем статику и сам endpoint статистики)
        if not request.url.path.startswith("/static") and request.url.path != "/api/statistics":
            request_count += 1
            total_response_time += process_time
        
        response.headers["X-Process-Time"] = str(process_time)
        return response

def get_average_response_time():
    """Получение среднего времени ответа в миллисекундах"""
    if request_count == 0:
        return 0
    return round((total_response_time / request_count) * 1000, 2)

@router.get("")
async def get_statistics(db: Session = Depends(get_db)):
    """Получение статистики сервиса"""
    
    # Количество пользователей
    users_count = db.query(func.count(User.id)).scalar()
    
    # Uptime сервиса (в секундах)
    uptime_seconds = time.time() - START_TIME
    
    # Конвертируем uptime в читаемый формат
    uptime_days = int(uptime_seconds // 86400)
    uptime_hours = int((uptime_seconds % 86400) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    
    # Среднее время ответа
    avg_response_time = get_average_response_time()
    
    return {
        "users_count": users_count,
        "uptime": {
            "days": uptime_days,
            "hours": uptime_hours,
            "minutes": uptime_minutes,
            "total_seconds": int(uptime_seconds)
        },
        "status": "online",
        "average_response_time_ms": avg_response_time,
        "total_requests_processed": request_count
    }
