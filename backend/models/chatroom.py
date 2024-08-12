from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from backend.models.user import User


class ChatRoom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    messages: list["Message"] = Relationship(back_populates="room")


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    time: int
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="chatroom.id")

    user: "User" = Relationship(back_populates="messages")  # type: ignore
    room: "ChatRoom" = Relationship(back_populates="messages")
