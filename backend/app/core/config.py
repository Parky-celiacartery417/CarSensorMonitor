from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://carsensor:carsensor_secret@db:5432/carsensor"
    SECRET_KEY: str = "k8s-prod-secret-xJ9mQ2vL7nR4wP1y"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    SCRAPE_INTERVAL_MINUTES: int = 60
    SCRAPE_MAX_PAGES_PER_MAKER: int = 3

    CARSENSOR_BASE_URL: str = "https://www.carsensor.net"

    MAKER_CODES: list[str] = [
        "TO",   # Toyota
        "HO",   # Honda
        "NI",   # Nissan
        "MZ",   # Mazda
        "SB",   # Subaru
        "SZ",   # Suzuki
        "DA",   # Daihatsu
        "MI",   # Mitsubishi
        "LE",   # Lexus
    ]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
