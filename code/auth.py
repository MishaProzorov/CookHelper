import bcrypt
import os
from authx import AuthX, AuthXConfig
from fastapi.templating import Jinja2Templates

#Ниче не менял
def get_password_hashe(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_COOKIE_SAMESITE = "lax"
config.JWT_COOKIE_SECURE = False
config.JWT_COOKIE_HTTP_ONLY = True
config.JWT_COOKIE_MAX_AGE = None  # Сессионный cookie — удаляется при закрытии браузера
security = AuthX(config=config)

current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))