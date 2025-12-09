from dotenv import load_dotenv
import os

load_dotenv()


def _env_list(name: str, default: str = ""):
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# CORS
ALLOWED_ORIGINS = _env_list("CORS_ALLOW_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000")
ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
ALLOWED_HEADERS = ["Authorization", "Content-Type", "X-CSRF-TOKEN", "Accept"]
ALLOW_CREDENTIALS = True


# Cookies / security flags
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "lax")
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() in ("1", "true", "yes")


def cors_options() -> dict:
    return {
        "allow_origins": ALLOWED_ORIGINS,
        "allow_credentials": ALLOW_CREDENTIALS,
        "allow_methods": ALLOWED_METHODS,
        "allow_headers": ALLOWED_HEADERS,
    }
