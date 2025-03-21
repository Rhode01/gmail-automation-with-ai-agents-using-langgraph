from fastapi import APIRouter
from app_backend.app.core.config import gmail_auth
from fastapi import Depends
from app_backend.app.utils.utils import GmailBase
from app_backend.app.schema.schema import GmailLabelRequest
router = APIRouter()


@router.get("/email/signup")
def root():
    service = gmail_auth.create_service()
    return
@router.post("/email/messages")
async def get_gmail_messages(request:GmailLabelRequest):
    gmail_base_obj = GmailBase(request.label)
    messages = gmail_base_obj.load_label_message()
    # for msg in messages:
    #     print(f"Subject: {msg['subject']}")
    #     print(f"Has attachment: {msg['has_attachment']}")
    #     if msg['attachments']:
    #         print(f"Attachments found: {[a['filename'] for a in msg['attachments']]}")
    return messages