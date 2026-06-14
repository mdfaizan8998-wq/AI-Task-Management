from fastapi import HTTPException,status,Request,Depends
from src.users.schemas import RegisterationSchema,LoginSchema,OtpSchema
from sqlmodel import Session
from src.users.models import UserTable, PendingUser
from pwdlib import PasswordHash
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random 
from jwt.exceptions import InvalidTokenError
from src.utils.verify_email import send_email
from src.users.database import get_db


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXP_TIME = os.getenv("EXP_TIME")

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)





def registration(body:RegisterationSchema, db:Session):
    otp = str(random.randint(100000, 999999))
   
    is_user = db.query(UserTable).filter(UserTable.email == body.email).first()
    # print("USER TABLE RESULT =", is_user)
    if is_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already Exist")
    
    
    
    
    hashed_password = get_password_hash(body.password)
    existing_user = db.query(PendingUser).filter(PendingUser.email == body.email).first()
    if existing_user:
        existing_user.name = body.name
        existing_user.username = body.username
        existing_user.hashed_password = hashed_password
        existing_user.otp = otp
        

    else:
        pending_user = PendingUser(
            name = body.name,
            username= body.username,
            email = body.email,
            hashed_password=hashed_password,
            otp = otp
        )
       
        db.add(pending_user)
        db.commit()
        db.refresh(pending_user)
        current_pending_email = pending_user.email
    
    

    send_email(body.email, f" Your OTP is {otp}")

    

    
    
    return pending_user


def verify(body:OtpSchema, db: Session):
    
    user = db.query(UserTable).filter(UserTable.email == body.email ).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already Verified")

   



    pending_user = db.query(PendingUser).filter(
        PendingUser.email == body.email
    ).first()
 


    if not pending_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if pending_user.otp != body.otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )
    
    try:
        new_user = UserTable(
            name=pending_user.name,
            username=pending_user.username,
            email=pending_user.email,
            hashed_password=pending_user.hashed_password,
            is_verified=True
        )

        db.add(new_user)
        db.delete(pending_user)
        db.commit()
        db.refresh(new_user)
    
    except Exception as e :
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Verification failed due to database error")

   
    return {
        "message": "Email verified successfully"
    }

def login(body:LoginSchema, db:Session):
     user = db.query(UserTable).filter(UserTable.email == body.email).first()
     if not user:
         raise HTTPException(status_code=404, detail="No account found with this email")
     
     if not verify_password(body.password, user.hashed_password):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")
     
     exp_time = datetime.now() + timedelta(minutes = int(EXP_TIME))
     

     token = jwt.encode({"_id":user.id,"exp": exp_time}, SECRET_KEY, algorithm=ALGORITHM)

     return {"token":token}


def is_auth(request:Request, db: Session = Depends(get_db)):
        
    try:

        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorize")
        
        token = token.split(" ")[-1]

        data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = data.get("_id")

        user = db.query(UserTable).filter(UserTable.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorize")


        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorize")

