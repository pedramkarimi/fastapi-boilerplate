from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # POSGRESQL 
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi_db"
    DB_USER: str = "fastapi_user"
    DB_PASSWORD: str = "fastapi_password"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    # JWT
    JWT_SECRET_KEY: str = "super-secret-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    # REDIS
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    # REDIS KEY 
    LOGIN_MAX_ATTEMPTS_PER_EMAIL: int = 5
    LOGIN_MAX_ATTEMPTS_PER_IP: int = 20
    LOGIN_ATTEMPT_WINDOW_SECONDS: int = 15 * 60  # پنجره شمارش تلاش‌ها (۱۵ دقیقه)
    LOGIN_LOCK_TTL_SECONDS: int = 15 * 60        # زمان قفل بودن (۱۵ دقیقه)
    RATELIMIT_DEFAULT_MAX_REQUESTS: int = 100
    RATELIMIT_DEFAULT_WINDOW_SECONDS: int = 60
    CACHED_DATA_TTL: int = 60

    # CORS
    BACKEND_CORS_ORIGINS : list[str]=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:8000"]
    
    class Config:
        env_file = ".env"   

settings = Settings()
