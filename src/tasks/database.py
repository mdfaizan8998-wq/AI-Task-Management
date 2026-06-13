from sqlmodel import create_engine, Session
from sqlmodel import SQLModel
from src.tasks.models import TasksUser
from src.users.models import UserTable



DATABASE_URL = "sqlite:///todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as db:
        yield db
