from fastapi import  APIRouter,Depends,status
from .schemas import UserCreateModel,UserModel,UserLoginModel
from.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .utils import create_access_token,decode_token,verify_passsword

auth_router=APIRouter()
user_service=UserService()

@auth_router.post('/signup',response_model=UserModel)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession=Depends(get_session)):
    email=user_data.email

    user_exists=await user_service.user_exists(email,session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    new_user=await user_service.create_user(user_data,session)

    return new_user

@auth_router.post('/login')

async def login_users(login_data:UserLoginModel,session:AsyncSession=Depends(get_session)):
    email=login_data.email
    password=login_data.password

    user=await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid=verify_passsword(password,user.password_hash)

        if password_valid:
            access_token=create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                }
            )

            return JSONResponse(
                content={
                    "message":"successful",
                    "access_token":access_token
                }
            )


    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN
    )
