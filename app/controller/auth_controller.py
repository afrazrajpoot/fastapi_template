from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma
from prisma.models import User
from ..services.auth_service import AuthService
from ..utils.schemas import SignInRequest

class AuthController:
    def __init__(self, prisma: Prisma):
        self.auth_service = AuthService(prisma)

    async def sign_in(self, signin_data: SignInRequest) -> dict:
        """Sign in user by email and return access token"""
        user = await self.auth_service.authenticate_user(signin_data.email)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.auth_service.create_access_token(data={"sub": user.email})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }

    async def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/signin"))) -> User:
        """Get current authenticated user"""
        user = await self.auth_service.get_current_user(token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
