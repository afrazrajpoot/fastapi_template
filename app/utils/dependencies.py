from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma
from prisma.models import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/signin")

def get_prisma() -> Prisma:
    """Get Prisma client instance"""
    return Prisma()

async def get_current_user(token: str = Depends(oauth2_scheme), prisma: Prisma = Depends(get_prisma)) -> User:
    """Get current authenticated user from JWT token"""
    from ..services.auth_service import AuthService

    auth_service = AuthService(prisma)
    user = await auth_service.get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user - can add additional checks here"""
    return current_user
