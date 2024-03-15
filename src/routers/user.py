from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from loguru import logger

from src.schemas.user import UserSchema, UserPublic, UserList
from src.models.user import User
from src.resources import get_session

router = APIRouter()


@router.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    logger.info('Creating a User.')

    user_db =  await session.scalar(
        select(User).where(User.username == user.username)
    )

    if user_db:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    user_db = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db


@router.get('/users/', response_model=UserList)
async def list_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    raw = await session.execute(select(User).offset(skip).limit(limit))
    users = raw.scalars().all()
    return {'users': users}


@router.put('/users/{user_id}', response_model=UserPublic)
async def update_user(user_id: int, user: UserSchema, session: AsyncSession = Depends(get_session)):
    user_db =  await session.scalar(
        select(User).where(User.id == user_id)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    user_db.username = user.username
    user_db.password = user.password
    user_db.email = user.email

    await session.commit()
    await session.refresh(user_db)

    return user_db


@router.delete('/users/{user_id}')
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(user_db)
    await session.commit()

    return {'message': 'User deleted'}
