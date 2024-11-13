from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, create_engine
from sqlalchemy.orm import relationship
from app.backend.db import Base, engine
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from app.models.user import User

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))

router = APIRouter()

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        tasks = db.scalars(select(Task)).all()
        return tasks

@router.get('/{task_id}')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        task = db.scalar(select(Task).where(Task.id == task_id))
        if task:
            return task
        else:
            raise HTTPException(status_code=404, detail="Task was not found")

@router.post('/create')
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        user = db.scalar(select(User).where(User.id == user_id))
        if user:
            new_task = task.dict()
            new_task["user_id"] = user_id
            db.execute(insert(Task).values(new_task))
            return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
        else:
            raise HTTPException(status_code=404, detail="User was not found")

@router.put('/update/{task_id}')
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        existing_task = db.scalar(select(Task).where(Task.id == task_id))
        if existing_task:
            db.execute(
                update(Task).where(Task.id == task_id).values(task.dict())
            )
            return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
        else:
            raise HTTPException(status_code=404, detail="Task was not found")

@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    async with db.begin():
        task = db.scalar(select(Task).where(Task.id == task_id))
        if task:
            db.execute(delete(Task).where(Task.id == task_id))
            return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deletion is successful!'}
        else:
            raise HTTPException(status_code=404, detail="Task was not found")