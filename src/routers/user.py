from fastapi import APIRouter, HTTPException, status
from loguru import logger

from src.schemas.user import UserSchema, UserPublic, UserDB, UserList

router = APIRouter()

database = []

@router.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(user: UserSchema):
    logger.info('Creating a User.')
    user_db = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_db)
    return user_db


@router.get('/users/', response_model=UserList)
async def list_users():
    return {'users': database}


@router.put('/users/{user_id}', response_model=UserPublic)
async def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_db = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_db

    return user_db


@router.delete('/users/{user_id}')
async def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del database[user_id - 1]

    return {'message': 'User deleted'}