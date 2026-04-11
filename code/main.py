from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from database import engine, Base
from api import auth_user, pages
from api import recipes
from api import statistics
from api.statistics import MetricsMiddleware

app = FastAPI()

# Добавляем middleware для измерения времени ответа
app.add_middleware(MetricsMiddleware)

current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(auth_user.router)
app.include_router(pages.router)
app.include_router(recipes.router)
app.include_router(statistics.router)