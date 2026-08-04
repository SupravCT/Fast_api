from .models import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from.utils import generate_password_hash,verify_passsword

class UserService:
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement=select(User).where(User.email==email)

        result=await session.exec(statement)

        data=result.first()

        return data

    async def user_exists(self,email,session:AsyncSession):
        user=await self.get_user_by_email(email,session)

        if user is None:
            return False
        else:
            return True

    async def create_user(self,user_data:UserCreateModel,session:AsyncSession):
        user_data_dict=user_data.model_dump()

        new_user=User(
            **user_data_dict
        )
        new_user.password_hash=generate_password_hash(user_data_dict['password'])

        new_user.role="user"

        session.add(new_user)

        await session.commit()

        return new_user


async def update_user(self,user:User,user_data,session:AsyncSession):

    for key,value in user_data.items():
        setattr(user,key,value)

    await session.commit()

    return user