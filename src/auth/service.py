from .models import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

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
        user_data_dict=user_data.model.dump()

        new_user=User(
            **user_data
        )
