from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# custom imports
from opendrive.uploaders.upload_routes import upload_router
from opendrive.account.routers import router as auth_router
from opendrive.db.config import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://[::1]:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Content-Type", "Authorization"],
)

app.include_router(auth_router)
app.include_router(upload_router)

