from fastapi.security import HTTPBearer
from fastapi import Request,Depends
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService

user_service=UserService()



class AccessTokenBearer(HTTPBearer):


    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        token = creds.credentials

        token_data =decode_token(token)

        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        if await token_in_blocklist(token_data['jti']):
             raise HTTPException(status_code=401, detail="Invalid or expired token")
            
        return token_data

    
access_token_bearer = AccessTokenBearer()


async def get_current_user(token_details:dict=Depends(access_token_bearer),
                     session:AsyncSession=Depends(get_session)):
    
    user_email=token_details['user']['email']

    user=await user_service.get_user_by_email(user_email,session)

    return user

