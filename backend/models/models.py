from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import datetime
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

    messages: List["Message"] = Relationship(back_populates="user")

class ChatRoom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    messages: List["Message"] = Relationship(back_populates="room")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="chatroom.id")

    user: User = Relationship(back_populates="messages")
    room: ChatRoom = Relationship(back_populates="messages")
