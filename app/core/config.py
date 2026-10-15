from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ecommerce Monolith"
    DEBUG: bool = True
    
    MYSQL_HOST: str = "db"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "ecommerce_user"
    MYSQL_PASSWORD: str = "ecommerce_pass"
    MYSQL_DB: str = "ecommerce_db"
    
    SECRET_KEY: str = "supersecretjwtkey_change_in_production_9f83a21b"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    class Config:
        env_file = ".env"

settings = Settings()