import os
from fastapi import Depends
from typing import Annotated, ClassVar
from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, '.env')


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        env_file_encoding="utf-8"
    )


settings = Settings()

engine = create_engine(settings.DATABASE_URL, echo=True)


def create_tables():
    print("Tables Created")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]

