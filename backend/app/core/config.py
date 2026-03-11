from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_SSL_REQUIRED: bool = False
    SSL_CA_PATH: str = ""

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Groq settings
    GROQ_API_KEY: str

    # App settings
    APP_NAME: str = "MedSync AI"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()