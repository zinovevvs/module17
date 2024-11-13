from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter()

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        users = db.scalars(select(User)).all()
        return users

@router.get('/{user_id}')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        user = db.scalar(select(User).where(User.id == user_id))
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User was not found")

@router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        new_user = user.dict()
        new_user["slug"] = slugify(new_user["username"])
        db.execute(insert(User).values(new_user))
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update/{user_id}')
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        existing_user = db.scalar(select(User).where(User.id == user_id))
        if existing_user:
            db.execute(
                update(User).where(User.id == user_id).values(user.dict())
            )
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
        else:
            raise HTTPException(status_code=404, detail="User was not found")

@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        existing_user = db.scalar(select(User).where(User.id == user_id))
        if existing_user:
            db.execute(delete(User).where(User.id == user_id))
            return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}
        else:
            raise HTTPException(status_code=404, detail="User was not found")
