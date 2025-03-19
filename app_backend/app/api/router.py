from fastapi import APIRouter
from app_backend.app.core.config import GmailAuth
from fastapi import Depends
router = APIRouter()


@router.get("/")
def root():
    gmail_auth = GmailAuth()
    response = gmail_auth.create_service()
    return response