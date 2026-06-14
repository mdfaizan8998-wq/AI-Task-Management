from fastapi import APIRouter, HTTPException, status, Depends,Request,BackgroundTasks
from src.users.schemas import RegisterationSchema,AuthResponseSchema,LoginSchema,OtpSchema
from sqlmodel import Session
from src.users.database import get_db
from src.users import controller

user = APIRouter(prefix="/auth",  tags=["Auth"])

@user.post("/registration", status_code=status.HTTP_201_CREATED)
def registraion(body:RegisterationSchema, db:Session = Depends(get_db),background_tasks: BackgroundTasks = BackgroundTasks()):
    return controller.registration(body, db,background_tasks)

@user.post("/verify",status_code=status.HTTP_200_OK)
def verify(body:OtpSchema, db:Session=Depends(get_db)):
    return controller.verify(body,db)


@user.post("/login",status_code=status.HTTP_200_OK)
def login(body:LoginSchema, db:Session = Depends(get_db)):
    return controller.login(body,db)

@user.get("/is_auth", response_model=AuthResponseSchema, status_code=status.HTTP_200_OK)
def is_authentication(request:Request, db:Session = Depends(get_db)):
    return controller.is_auth(request,db)
