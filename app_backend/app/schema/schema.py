from pydantic import BaseModel, Field
from typing import Optional
class GmailLabelRequest(BaseModel):
    label: str = Field(
        default="INBOX",
        description="Gmail label name (case-insensitive)",
        example="Important"
    )
    max_results: Optional[int] = Field(
        default=5,
        ge=1,
        le=500,
        description="Maximum number of messages to retrieve (1-500)"
    )

class MessageIdRequest(BaseModel):
    message_id: str = Field(
        ...,
        description="Gmail message ID",
        example="18c7d7a9a8d7a9d7",
        min_length=16,
        max_length=32
    )

class SendMessageRequest(BaseModel):
    to: str = Field(
        ...,
        description="Recipient email address",
        example="recipient@example.com",
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    subject: str = Field(
        ...,
        description="Email subject line",
        example="Meeting Reminder",
        max_length=255
    )
    body: str = Field(
        ...,
        description="Email body content",
        example="Don't forget our meeting tomorrow at 10 AM."
    )

class ReplyMessageRequest(BaseModel):
    message_id: str = Field(
        ...,
        description="Original message ID to reply to",
        example="18c7d7a9a8d7a9d7"
    )
    reply_body: str = Field(
        ...,
        description="Content of the reply message",
        example="Thank you for your email. I'll respond shortly."
    )
    quote_original: bool = Field(
        default=True,
        description="Include original message in reply"
    )