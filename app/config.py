from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str
    database_username: str
    secret_key: str
    database_hostname: str
    database_port: str
    database_name: str
    algorithm : str
    access_token_expire_time: str
    class Config:
        # This tells Pydantic to look for a .env file automatically
        env_file = ".env"

# This instance is what you import in main.py or database.py
settings = Settings()
