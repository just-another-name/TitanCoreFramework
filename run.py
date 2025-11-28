# run.py
from app.main import app
from config.app import settings
from urllib.parse import urlparse

if __name__ == "__main__":
    import uvicorn
    
    # Парсим URL из appBaseUrl
    parsed_url = urlparse(settings.appBaseUrl)
    host = parsed_url.hostname or "127.0.0.1"
    port = parsed_url.port or 8000
    
    uvicorn.run(
        app, 
        host=host,
        port=port
    )