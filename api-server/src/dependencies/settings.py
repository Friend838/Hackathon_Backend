from functools import lru_cache

from src.config.config import Settings


@lru_cache()
def get_settings():
    return Settings()
