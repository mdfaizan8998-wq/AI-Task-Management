from sqlmodel import SQLModel, Field,ForeignKey,Column
from datetime import datetime,timezone
from enum import Enum



class Taskstatus(str, Enum):
    PENDING ="PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

user_input = "pending"
status = Taskstatus(user_input.upper())


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


user_input = "medium"
priority = Priority(user_input.upper())




class TasksUser(SQLModel, table=True):
    __tablename__ = "tasks"

    id : int | None = Field(default=None, primary_key=True)

    title : str 
    description : str

    status : Taskstatus = Field(default=Taskstatus.PENDING)
    priority : Priority = Field(default=Priority.MEDIUM)

    updated_at : datetime |None = Field(default = None,
                                  sa_column_kwargs={"onupdate": lambda:datetime.now(timezone.utc)})
    created_at : datetime = Field(default_factory=datetime.now)

    due_date : datetime

    user_id : int = Field( sa_column=Column(ForeignKey("users.id", ondelete="CASCADE" )))