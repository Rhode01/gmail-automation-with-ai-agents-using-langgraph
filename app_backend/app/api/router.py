from fastapi import APIRouter, HTTPException, status
from app_backend.app.core.config import gmail_auth
from app_backend.app.utils.utils import GmailBase, GmailCRUDBase
from app_backend.app.schema.schema import (
    GmailLabelRequest,
    MessageIdRequest,
    SendMessageRequest,
    ReplyMessageRequest
)
from typing import Dict, List
router = APIRouter()

@router.get("/email/auth-status")
def check_auth_status() -> Dict[str, bool]:
    service = gmail_auth.create_service()
    return {"authenticated": service is not None}

@router.post("/email/messages", response_model=List[Dict])
async def get_gmail_messages(request: GmailLabelRequest):
    try:
        gmail_base = GmailBase(request.label, max_results=request.max_results)
        messages = gmail_base.load_label_message()
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve messages: {str(e)}"
        )

@router.post("/email/message", response_model=Dict)
async def read_email(request: MessageIdRequest):
    try:
        gmail_base = GmailBase(label="INBOX")
        crud = GmailCRUDBase(gmail_base)
        result = crud.read_email(request.message_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return result
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading message: {str(e)}"
        )

@router.post("/email/send")
async def send_email(request: SendMessageRequest):
    try:
        gmail_base = GmailBase(label="SENT") 
        crud = GmailCRUDBase(gmail_base)
        result = crud.create_email(
            to=request.to,
            subject=request.subject,
            body=request.body
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )

@router.post("/email/reply")
async def reply_to_email(request: ReplyMessageRequest):
    try:
        gmail_base = GmailBase(label="INBOX") 
        crud = GmailCRUDBase(gmail_base)
        result = crud.reply_to_email(
            message_id=request.message_id,
            reply_body=request.reply_body,
            quote_original=request.quote_original
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send reply: {str(e)}"
        )

@router.delete("/email/delete")
async def delete_email(request: MessageIdRequest):
    try:
        gmail_base = GmailBase(label="INBOX")
        crud = GmailCRUDBase(gmail_base)
        result = crud.delete_email(request.message_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete email: {str(e)}"
        )