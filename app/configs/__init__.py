import os
from functools import lru_cache

from app.configs.dev import DevSettings


@lru_cache
def get_settings() -> DevSettings:
    load_mode = os.getenv("MODE")
    match load_mode.upper():
        case "DEV" | "LOCAL" | "TEST":
            return DevSettings()


settings = get_settings()
