from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.entity.models import Todo, User
from src.schemas.todo import TodoSchema, TodoUpdateSchema


async def get_todos(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = (
        select(Todo)
        .where(Todo.user_id == user.id)
        .offset(offset)
        .limit(limit)
        .options(selectinload(Todo.user))
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_todos(limit: int, offset: int, db: AsyncSession):
    stmt = select(Todo).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_todo(todo_id: int, db: AsyncSession, user: User):
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_todo(body: TodoSchema, db: AsyncSession, user: User):
    todo = Todo(**body.model_dump(exclude_unset=True), user_id=user.id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(todo_id: int, body: TodoUpdateSchema, db: AsyncSession, user: User):
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()

    if todo:
        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        await db.commit()
        await db.refresh(todo)

    return todo


async def delete_todo(todo_id: int, db: AsyncSession, user: User):
    stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()

    if todo:
        await db.delete(todo)
        await db.commit()

    return todo
