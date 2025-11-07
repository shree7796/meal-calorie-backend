from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    USDA_API_KEY: str
    USDA_BASE_URL: str = "https://api.nal.usda.gov/fdc/v1/foods/search"
    PAGE_SIZE: int = 10

    DATABASE_URL: str = "sqlite:///./dev.db"
    RATE_LIMIT: str = "15/minute"

    class Config:
        env_file = ".env"

settings = Settings()
