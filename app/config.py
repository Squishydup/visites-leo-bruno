import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    redis_url: str = field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )


settings = Settings()
