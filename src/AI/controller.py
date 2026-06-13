from src.AI.schemas import suggest_description
from src.AI.service import graph
from src.users.models import UserTable
from src.AI.service import TaskAutomationController
from fastapi import Depends,HTTPException,status
from src.users.controller import is_auth

async def suggest_task(body: suggest_description):
    if not body.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Task title cannot be empty"
        )
    # automation_controller = TaskAutomationController()
    try:
        
        result = graph.invoke({
            "title": body.title,
            
        })
        description = result.get("description", "No description generated")
        tag = result.get("tag", "#Personal")
        return {
            "title": body.title,
            "description": description,
            "tag": tag
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Graph Error: {str(e)}"
        )
