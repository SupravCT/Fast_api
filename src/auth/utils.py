from passlib.context import CryptContext
from datetime import timedelta,datetime
import jwt
from src.config import settings

password_context=CryptContext(
    schemes=['bcrypt']

)



def generate_password_hash(password:str):
    hash=password_context.hash(password)

    return hash

def verify_passsword(password:str,hash_password:str):
    return password_context.verify(password,hash_password)

def create_access_token(user_data,expiry:timedelta=timedelta(hours=1)):

    payloadd={}
    payloadd['user']=user_data
    payloadd['exp']=datetime.now()+expiry

    token=jwt.encode(
        payload=payloadd,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token