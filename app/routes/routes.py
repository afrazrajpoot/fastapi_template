from fastapi import APIRouter, Depends
from app.controller.hello_controller import HelloController
from app.utils.dependencies import get_current_active_user
from prisma.models import User

router = APIRouter()

def get_hello_controller() -> HelloController:
    """Dependency injection for HelloController"""
    return HelloController()

@router.get("/hello")
async def hello_world(controller: HelloController = Depends(get_hello_controller)):
    """Simple hello world endpoint (public)"""
    return await controller.get_hello()

@router.get("/hello/protected")
async def hello_world_protected(
    controller: HelloController = Depends(get_hello_controller),
    current_user: User = Depends(get_current_active_user)
):
    """Protected hello world endpoint (requires authentication)"""
    result = await controller.get_hello()
    result["message"] = f"Hello {current_user.name or current_user.email}! Welcome to Purposify API!"
    result["user"] = {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }
    return result
