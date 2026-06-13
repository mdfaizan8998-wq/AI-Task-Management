from sqlmodel import SQLModel 
from pydantic import EmailStr


class RegisterationSchema(SQLModel):
    name : str
    username : str
    email : EmailStr
    password : str
 


            


class AuthResponseSchema(SQLModel):
    id : int
    name : str
    username : str
    email : EmailStr
    

class LoginSchema(SQLModel):
    email : EmailStr
    password : str

class OtpSchema(SQLModel):
    email : EmailStr
    otp : str