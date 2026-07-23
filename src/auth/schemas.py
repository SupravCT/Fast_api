from pydantic import BaseModel,Field
from uuid import UUID
from datetime import datetime

class UserCreateModel(BaseModel):

    username:str=Field(max_length=8)
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)
    first_name: str
    last_name: str

class UserModel(BaseModel):
        uid:UUID
        username:str
        email:str
        first_name:str
        last_name:str
        is_verified:bool=Field(default=False)
    
        password_hash:str=Field(exclude=True)
    
        created_at: datetime 
        updated_at: datetime
    