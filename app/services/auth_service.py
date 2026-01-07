from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from prisma import Prisma
from prisma.models import User

from ..utils.config import settings

class AuthService:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def authenticate_user(self, email: str) -> Optional[User]:
        """Authenticate user by email - checks if user exists"""
        user = await self.prisma.user.find_unique(where={"email": email})
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token (no expiration)"""
        to_encode = data.copy()

        # Comment out expiration for non-expiring tokens
        # if expires_delta:
        #     expire = datetime.utcnow() + expires_delta
        # else:
        #     expire = datetime.utcnow() + timedelta(minutes=15)
        #
        # to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
        except JWTError:
            return None

        user = await self.prisma.user.find_unique(where={"email": email})
        return user
