from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )  
    
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "your-secret-key-change-in-production"

    HOST: str 
    PORT: int = 8000
    RELOAD: bool = True

    DATABASE_URL: str
    DATABASE_ECHO: bool = False

settings = Settings()

