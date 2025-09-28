from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# custom imports
from opendrive.uploaders.upload_routes import upload_router
from opendrive.account.routers import router as auth_router
from opendrive.db.config import create_tables, engine, SessionDependency


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(upload_router)
app.include_router(auth_router)

origins = [
    "your_api"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     # Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],
)


