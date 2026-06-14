from sqlmodel import SQLModel,Field
from datetime import datetime,timezone
from pydantic import EmailStr





class UserTable(SQLModel, table=True):
    __tablename__ ="users"


    id : int | None = Field(default=None, primary_key=True)

    name : str 
    username : str 
    email : EmailStr = Field(unique=True, index=True)
    hashed_password : str
    updated_at : datetime | None = Field(default_factory=None, sa_column_kwargs={"onupdate":lambda:datetime.now(timezone.utc)})

    is_active : bool = Field(default=True)
    created_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    
    is_verified : bool = Field(default=True)


class PendingUser(SQLModel, table=True):
    __tablename__ = "pending_user"

    id : int | None = Field(default=None, primary_key=True)
    name : str 
    username : str 
    email : EmailStr = Field(unique=True,index=True)
    hashed_password : str
    otp : str
