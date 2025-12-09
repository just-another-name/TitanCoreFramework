import logging
import os
import threading
import time
from typing import Dict, Tuple, Optional

import redis


class RateLimitService:
    """
    Rate limiter with Redis backend; falls back to in-memory if Redis недоступен.
    Для прод рекомендуется Redis (шарится между воркерами/хостами).
    """

    _attempts: Dict[str, Tuple[int, float]] = {}
    _lock = threading.Lock()

    _redis_client: Optional[redis.Redis] = None
    _redis_enabled = False
    _logger = logging.getLogger(__name__)
    _redis_script = None

    @classmethod
    def _init_redis(cls) -> None:
        if cls._redis_enabled:
            return
        url = os.getenv("RATE_LIMIT_REDIS_URL")
        if not url:
            return
        try:
            client = redis.Redis.from_url(url, decode_responses=True)
            client.ping()
            # Lua-скрипт для атомарного INCR + EXPIRE
            script = """
            local current = redis.call('INCR', KEYS[1])
            if current == 1 then
                redis.call('PEXPIRE', KEYS[1], ARGV[1])
            end
            return current
            """
            cls._redis_script = client.register_script(script)
            cls._redis_client = client
            cls._redis_enabled = True
            cls._logger.info("RateLimitService: Redis backend enabled")
        except Exception as exc:  # pragma: no cover - логирование отказа
            cls._logger.warning(f"RateLimitService: Redis disabled ({exc})")
            cls._redis_enabled = False
            cls._redis_client = None
            cls._redis_script = None

    @classmethod
    def _redis_check(cls, key: str, limit: int, window_seconds: int) -> Optional[bool]:
        cls._init_redis()
        if not cls._redis_enabled or not cls._redis_client or not cls._redis_script:
            return None
        try:
            # возвращает количество попыток
            attempts = cls._redis_script(keys=[key], args=[window_seconds * 1000], client=cls._redis_client)
            return int(attempts) <= limit
        except Exception as exc:  # pragma: no cover - логирование отказа
            cls._logger.warning(f"RateLimitService: Redis check failed ({exc}), falling back to memory")
            cls._redis_enabled = False
            return None

    @classmethod
    def check_and_increment(cls, key: str, limit: int, window_seconds: int) -> bool:
        """
        Returns True if within limit; increments attempt counter.
        Tries Redis first; if недоступен — in-memory fallback.
        """
        redis_result = cls._redis_check(key, limit, window_seconds)
        if redis_result is not None:
            return redis_result

        now = time.monotonic()
        with cls._lock:
            attempts, window_start = cls._attempts.get(key, (0, now))

            # Reset window if expired
            if now - window_start >= window_seconds:
                attempts = 0
                window_start = now

            attempts += 1
            cls._attempts[key] = (attempts, window_start)

            return attempts <= limit