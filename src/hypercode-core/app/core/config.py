from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    REDIS_URL: str = "redis://redis:6379"
    POSTGRES_URL: str = "postgresql://postgres:changeme@postgres:5432/hypercode"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

def get_settings():
    return settings
