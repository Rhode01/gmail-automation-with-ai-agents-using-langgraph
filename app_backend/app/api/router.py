from fastapi import APIRouter
from app_backend.app.core.config import gmail_auth
from fastapi import Depends
router = APIRouter()


@router.get("/")
def root():
    service = gmail_auth.create_service()
    return 