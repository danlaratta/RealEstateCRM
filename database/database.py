import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Env variables
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USERNAME: str = os.getenv('DB_USERNAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_PORT: str = os.getenv('DB_PORT')

    @property # decorator makes this method act like an attribute
    def DATABASE_URL(self) -> str:
        return f'postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@localhost:{self.DB_PORT}/{self.DB_NAME}'

    #  tells Pydantic to load the variables above from .env
    class Config:
        env_file = '.env'


settings = Settings()
engine = create_engine(settings.DATABASE_URL) # creates a connection to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # manages database transactions (each request gets a new session from SessionLocal())
Base = declarative_base() # base class for all SQLAlchemy models