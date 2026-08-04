from fastapi import  APIRouter,Depends,status
from .schemas import UserCreateModel,PasswordResetConfirmationModel,UserModel,PasswordResetRequestModel,UserLoginModel
from.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .utils import create_access_token,verify_passsword,create_url_safe_token,decode_url_safe_token
from src.db.redis import add_jti_to_blocklist
from .dependencies import AccessTokenBearer,get_current_user,RoleChecker
from src.mail import create_message,mail
from src.config import settings



auth_router=APIRouter()
user_service=UserService()
access_token_bearer = AccessTokenBearer()
role_checker=RoleChecker(['admin','user'])

@auth_router.post('/signup',response_model=UserModel)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession=Depends(get_session)):
    email=user_data.email

    user_exists=await user_service.user_exists(email,session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    new_user=await user_service.create_user(user_data,session)

    token=create_url_safe_token({"email": email})

    Link=f"http://{settings.DOMAIN}/api/v1/auth/verify{token}"

    html_message=f'''
    <h1>Welcome to our platform</h1>
    <h2>verify your email address</h2>
    <p>Click the link below to verify your email address:</p>
    <a href="{Link}">to Verify Email</a>
    '''
    message=create_message(
        recipients=[email],
        subject="Verify your email address",
        body=html_message
    )

    await mail.send_message(message)

    return {
        "message":"User created successfully",
        "user":new_user
    }


@auth_router.get('/verify/{token}')
async def verify_usr_acc(token,session:AsyncSession=Depends(get_session)):
    token_data=decode_url_safe_token(token)

    user_email=token_data.get('email')

    if user_email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid token")
    else:
        user=await user_service.get_user_by_email(user_email,
                                            session=session)


        await user_service.update_user(user,{'is_verified':True},session)

        return JSONResponse(content=
        {"message": "Email verified successfully"})
    


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
                    'user_uid':str(user.uid),
                    'role':user.role
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

@auth_router.get('/me')
async def get_me(user=Depends(get_current_user),
                 _:bool=Depends(role_checker)):
    return user

@auth_router.post('/logout')
async def revoke_token(token_details: dict = Depends(access_token_bearer)):
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"},
        status_code=status.HTTP_200_OK
    )

@auth_router.post('/send-mail')
async def send_mail():
    html="<h1>Hello from FastAPI</h1>"
    message = create_message(
        recipients=["supravchand2@gmail.com"],
        subject="Test Email",
        body=html
    )
    await mail.send_message(message)
    return {"message": "Email sent"}


@auth_router.post('/password_reset_request')
async def password_reset(email_data:PasswordResetRequestModel):
    email=email_data.email

    token=create_url_safe_token({"email":email})

    link=f"http://{settings.DOMAIN}/api/v1/auth/password_reset/{token}"

    html_message=f'''
    <h1>Password Reset Request</h1>
    <p>click <a href="{link}">here</a> to reset your password</p>
    '''

    message=create_message(
        recipients=[email],
        subject="Password Reset Request",
        body=html_message

    )

    await mail.send_message(message)

    return {
        "message":"Password reset email sent successfully"

    }



@auth_router.get('/password_reset/{token}')
async def change_password(token,
                          password:PasswordResetConfirmationModel,
                          session:AsyncSession=Depends(get_session)):

    if password.new_password != password.confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Passwords do not match")

    token_data=decode_url_safe_token(token)

    user_email=token_data.get('email')

    if user_email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid token")
    else:
        user=await user_service.get_user_by_email(user_email,
                                            session=session)


        await user_service.update_user(user,{'is_verified':True},session)

        return JSONResponse(content=
        {"message": "Email verified successfully"})


    
