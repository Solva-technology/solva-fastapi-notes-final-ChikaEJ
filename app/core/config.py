from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    _instance = None

    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SECRET_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance



settings = Settings()
