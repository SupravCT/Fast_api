from fastapi.security import HTTPBearer
from fastapi import Request
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist



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
