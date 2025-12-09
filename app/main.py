# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware 
import logging.config
import sys
from pathlib import Path
import os


sys.path.append(str(Path(__file__).parent.parent))

from config import route
from config.app import settings
from config.logging import LOGGING
from config.security import cors_options, SESSION_COOKIE_SAMESITE

session_secret = os.getenv("SESSION_SECRET_KEY")
if not session_secret or len(session_secret) < 32:
    raise RuntimeError("SESSION_SECRET_KEY must be set and at least 32 characters long")

app = FastAPI(title=settings.app_base_name)

logging.config.dictConfig(LOGGING)

# https_only только в production для работы в development без HTTPS
https_only = settings.environment == "production"

app.add_middleware(
    SessionMiddleware,
    secret_key = session_secret,
    session_cookie="session",      
    max_age=60 * 60 * 24 * 7,
    same_site=SESSION_COOKIE_SAMESITE,
    https_only=https_only
)

# CORS (конфигурируется через переменные окружения)
app.add_middleware(
    CORSMiddleware,
    **cors_options()
)

app.include_router(route.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

