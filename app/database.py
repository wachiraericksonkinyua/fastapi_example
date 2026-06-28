import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from .config import settings
# # Load the variables from the .env file
# load_dotenv()
# 1. Explicitly locate the .env file relative to this file (database.py)
# env_path = Path(__file__).resolve().parent / ".env"
# load_dotenv(dotenv_path=env_path)

# # Fetch variables
# user = os.getenv("DATABASE_USERNAME")
# password = os.getenv("DATABASE_PASSWORD")
# host = os.getenv("DATABASE_HOSTNAME")
# port = os.getenv("DATABASE_PORT")
# name = os.getenv("DATABASE_NAME")

# 3. Validation: Stop the app if crucial variables are missing (prevents "None" errors)
# if not all([user, host, port, name]):
#     raise EnvironmentError("Missing database environment variables in .env file!")
# # Construct the URL
#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# Simply use the URL directly
SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
