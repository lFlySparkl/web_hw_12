from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.entity.models import User
from src.schemas.user import UserCreate


async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).filter_by(email=email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(body: UserCreate, db: AsyncSession):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def confirm_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    if user:
        user.confirmed = True
        await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    if not user:
        raise ValueError("User not found")
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
