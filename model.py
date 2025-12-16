from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime ,UTC


class ChatRoom(SQLModel, table=True):
    __tablename__ = "chat_rooms"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    join_id: str = Field(unique=True, index=True, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


class JoinId(SQLModel):
    """Pydantic model for API responses/requests"""
    join_id: str


'''model for the chat messages'''

class ChatMessage(BaseModel):
    sender : str
    message : str
    timestamp : datetime = datetime.now(UTC)
