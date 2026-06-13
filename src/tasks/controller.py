from fastapi import HTTPException, status
from src.tasks.schemas import TaskSchema,TaskUpdateSchema
from sqlmodel import Session, select
from src.tasks.models import TasksUser




def all_tasks(db:Session, user:TasksUser):

    tasks = db.exec(select(TasksUser).filter(TasksUser.user_id == user.id)).all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Not able to see somone tasks")
    return tasks

def one_task(id:int,db:Session, user:TasksUser):

    task = db.exec(select(TasksUser).where(TasksUser.id == id, TasksUser.user_id == user.id)).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    
    return task




def create(body:TaskSchema, db:Session, user:TasksUser):


    task = TasksUser(
        title = body.title,
        description = body.description,
        status = body.status,
        priority = body.priority,
        due_date = body.due_date,
        user_id = user.id
    )


    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update(id:int, body:TaskUpdateSchema, db:Session, user:TasksUser):

    task = db.get(TasksUser,id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not allowed to update this Task")

    
    update_task = body.model_dump(exclude_unset=True)

    for key, value in update_task.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delet(id:int, db:Session, user:TasksUser):

    task = db.get(TasksUser,id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to delete this Task")
        
    
    db.delete(task)
    db.commit()

    return None