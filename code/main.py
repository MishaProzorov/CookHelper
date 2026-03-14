from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from database import engine, Base
from api import auth_user, pages
from api import recipes
app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(auth_user.router)
app.include_router(pages.router)

app.include_router(recipes.router)