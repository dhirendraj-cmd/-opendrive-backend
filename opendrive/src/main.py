from fastapi import FastAPI
from opendrive.uploaders.upload_routes import upload_router


app = FastAPI()

app.include_router(upload_router)




