from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    created_at: int = Field(default=round(datetime.now().timestamp()))
    
    messages: list["Message"] = Relationship(back_populates="user")  # type: ignore
