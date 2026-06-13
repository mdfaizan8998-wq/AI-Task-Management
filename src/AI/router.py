from fastapi import APIRouter, Depends, status
from src.AI.schemas import suggest_description
from src.AI import controller
from src.users.controller import is_auth
from src.users.models import UserTable


ai = APIRouter(tags=["Ask-AI"])


@ai.post("/suggest",status_code=status.HTTP_200_OK)
async def suggest(body:suggest_description):
    return await controller.suggest_task(body)