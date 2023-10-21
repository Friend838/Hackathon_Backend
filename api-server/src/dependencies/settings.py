from functools import lru_cache

# pylint: disable=import-error
from src.config.config import Settings


@lru_cache()
def get_settings():
    return Settings()
