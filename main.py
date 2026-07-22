'''from fastapi import FastAPI, Header,status
from typing import Optional,Literal
from pydantic import BaseModel


app=FastAPI()

@app.get("/")

async def home():
    return {"message": "Hello, World!"}

@app.get("/greet")

async def greet(name: Optional[str] = None, age: Optional[int] = 0):
    if name is None:
        return {"message": "Hello, Stranger!", "age": age}
    return {"message": f"Hello, {name}!", "age": age}

class UserModel(BaseModel):
    name:str
    age:int
    gender:Literal["male","female"]

@app.post('/create_user')

async def create_user(user_data:UserModel):
    return{
        "name":user_data.name,
        "age":user_data.age,
        "gender":user_data.gender
    } 

@app.get('/get_headers')

async def get_headers(
    accept:str=Header(None),
    content_type:str=Header(None),
    user_agent:Optional[str]=Header(None)
):
    request_header={}
    request_header["Accept"]=accept
    request_header["Content-Type"]=content_type
    request_header["User-Agent"]=user_agent
    return request_header



'''