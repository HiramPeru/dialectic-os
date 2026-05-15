from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql://dialectic:dialectic@localhost:5432/dialectic'
    REDIS_URL: str = 'redis://localhost:6379/0'
    class Config:
        env_file = '.env'

settings = Settings()
