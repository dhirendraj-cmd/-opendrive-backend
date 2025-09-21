from fastapi import FastAPI
from opendrive.uploaders.upload_routes import upload_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

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




