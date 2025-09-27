import os, secrets
from fastapi import Depends
from typing import Annotated, ClassVar
from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict


# import for secret_key
from dotenv import load_dotenv, find_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, '.env')


# generate secret key function if secret key not present
def generate_secret_if_not_present():
    # here we generate secret key if not there and pass it in our other modules if not env_file or "SECRET_KEY" not in open(DOTENV_PATH).read():
    env_file = find_dotenv(DOTENV_PATH)
    if not env_file or not os.getenv("SECRET_KEY") or "SECRET_KEY" not in open(DOTENV_PATH).read():
        secret=secrets.token_urlsafe(32)
        with open(DOTENV_PATH, "a") as out:
            out.write(f"\nSECRET_KEY={secret}\n")
        print("new secret key is generated and added")


generate_secret_if_not_present()

load_dotenv(DOTENV_PATH)


class Settings(BaseSettings):
    DATABASE_URL: str
    ALGORITHM: str
    SECRET_KEY: str

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

