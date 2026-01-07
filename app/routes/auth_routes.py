from fastapi import APIRouter, Depends
from ..controller.auth_controller import AuthController
from ..utils.schemas import SignInRequest, Token, UserResponse
from ..utils.dependencies import get_prisma, get_current_active_user

router = APIRouter()

def get_auth_controller(prisma = Depends(get_prisma)) -> AuthController:
    """Dependency injection for AuthController"""
    return AuthController(prisma)

@router.post("/signin", response_model=Token)
async def sign_in(
    signin_data: SignInRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Sign in endpoint - returns JWT access token for existing user"""
    return await controller.sign_in(signin_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user = Depends(get_current_active_user)
):
    """Get current authenticated user info"""
    return current_user
