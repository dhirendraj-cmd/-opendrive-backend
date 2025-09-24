import os
from fastapi import Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# DB_USER=config('DB_USER')
# DB_PASS=config('DB_PASS')
# DB_NAME=config('DB_NAME')
# DB_HOST=config('DB_HOST')
# DB_PORT=config('DB_PORT')

# class Settings(BaseSettings):

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    print("Tables Created")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]

