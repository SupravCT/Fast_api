from pydantic import BaseModel
from sqlmodel import SQLModel,Field,Column
from datetime import datetime
from uuid import UUID,uuid4
from sqlalchemy.dialects import postgresql
from typing import Optional


class Book(SQLModel,table=True):
    __tablename__="BOOKS"

    uid:UUID=Field(
        sa_column=Column(
            postgresql.UUID,
            nullable=False,
            primary_key=True,
            default=uuid4
        )
    )
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str
    user_uid:Optional[UUID]=Field(default=None,foreign_key="users.uid")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<Book{self.title}>"