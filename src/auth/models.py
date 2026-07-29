from sqlmodel import SQLModel,Field,Column
from datetime import datetime
from uuid import UUID,uuid4
from sqlalchemy.dialects import postgresql
from datetime import datetime 

class User(SQLModel,table=True):

    __tablename__="users"
    uid:UUID=Field(
        sa_column=Column(
            postgresql.UUID,
            primary_key=True,
            nullable=False,
            default=uuid4

        )
    )
    username:str
    email:str
    first_name:str
    last_name:str
    role:str=Field(default="user")
    is_verified:bool=Field(default=False)

    password_hash:str=Field(exclude=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User{self.username}>"