from fastapi import FastAPI
from app_backend.app.api.router import router
app = FastAPI()
app.include_router(router)