from passlib.context import CryptContext
from datetime import timedelta,datetime
import jwt
from src.config import settings
import logging
import uuid
from itsdangerous import URLSafeTimedSerializer

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
    payloadd['jti'] = str(uuid.uuid4())

    token=jwt.encode(
        payload=payloadd,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_token(token):
    try:
        token_data=jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

def create_url_safe_token(data):
    serializer=URLSafeTimedSerializer(
        secret_key=settings.JWT_SECRET_KEY,
        salt=settings.JWT_ALGORITHM
    )
    token=serializer.dumps(data)
    return token

def decode_url_safe_token(token):
    try:
        seralizer=URLSafeTimedSerializer(
            secret_key=settings.JWT_SECRET_KEY,
            salt=settings.JWT_ALGORITHM
        )
        token_data=seralizer.loads(token)
        return token_data
    except Exception as e:
        logging.exception(e)
        return None