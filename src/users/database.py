from sqlmodel import SQLModel 
from src.users.models import  PendingUser,UserTable
from sqlmodel import create_engine, Session



DATABASE_URL = "sqlite:///user.db"
PENDING_DB_URL = "sqlite:///pending_users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

pending_engine = create_engine(PENDING_DB_URL, connect_args={"check_same_thread": False})

def create_db():
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    SQLModel.metadata.create_all(pending_engine)

def get_db():
    with Session(engine) as db:
        yield db
    # print(db.query(UserTable).all())

def get_db():
    with Session(pending_engine) as db:
        yield db

# if __name__ == "__main__":
#     create_db()
  
