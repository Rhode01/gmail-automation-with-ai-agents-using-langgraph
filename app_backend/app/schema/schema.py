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
    