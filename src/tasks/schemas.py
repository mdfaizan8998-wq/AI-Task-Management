from sqlmodel import SQLModel
from src.tasks.models import Taskstatus, Priority
from datetime import datetime





class TaskSchema(SQLModel):
    title : str
    description  : str
    status : Taskstatus
    priority : Priority
    due_date : datetime



class TaskUpdateSchema(SQLModel):
    title : str  |None = None
    description  : str |None = None
    status : Taskstatus |None = None
    priority : Priority |None = None
    due_date : datetime |None = None



class TaskResponseSchema(SQLModel):
    id : int
    title : str
    description  : str
    status : Taskstatus
    priority : Priority
    due_date : datetime
