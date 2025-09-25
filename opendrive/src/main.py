from fastapi import FastAPI
from opendrive.uploaders.upload_routes import upload_router
from fastapi.middleware.cors import CORSMiddleware
from opendrive.db.config import create_tables, engine, SessionDependency
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(upload_router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     # Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],
)


