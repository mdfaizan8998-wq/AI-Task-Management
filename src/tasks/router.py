from fastapi import APIRouter , Depends,status
from src.tasks.schemas import TaskSchema,TaskUpdateSchema,TaskResponseSchema
from sqlmodel import Session
from src.tasks.database import get_db
from src.tasks import controller
from typing import List
from src.users.controller import is_auth
from src.tasks.models import TasksUser


router = APIRouter(tags=["Tasks"])

@router.get("/all_task", response_model=List[TaskResponseSchema], status_code=status.HTTP_200_OK)
def all_task(db:Session = Depends(get_db), user:TasksUser = Depends(is_auth)):
    return controller.all_tasks(db,user)

@router.get("/one_task/{id}",response_model=TaskResponseSchema, status_code=status.HTTP_200_OK)
def one_task(id:int,db:Session = Depends(get_db), user:TasksUser = Depends(is_auth)):
    return controller.one_task(id,db,user)

@router.post("/create", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create(body:TaskSchema, db:Session = Depends(get_db), user:TasksUser = Depends(is_auth)):
    return controller.create(body,db,user)

@router.put("/update/{id}", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def update(id:int,body:TaskUpdateSchema, db:Session = Depends(get_db), user:TasksUser = Depends(is_auth)):
    return controller.update(id,body,db,user)

@router.delete("/delete/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db:Session = Depends(get_db), user:TasksUser = Depends(is_auth)):
    return controller.delet(id,db, user)