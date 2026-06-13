from fastapi import FastAPI
from src.tasks.router import router
from src.users.router import user
from src.AI.router import ai
from src.users.database import create_db
from src.tasks.database import create_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="This is  My Tasks Management App With GenAI")

create_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development me clear testing ke liye allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(user)
app.include_router(ai)
