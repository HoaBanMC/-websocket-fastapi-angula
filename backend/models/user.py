from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

    messages: list["Message"] = Relationship(back_populates="user")  # type: ignore
