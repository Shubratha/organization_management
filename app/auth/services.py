from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import SuperAdminDAO
from app.auth.schemas import SuperAdminLogin, Token
from app.core.security import create_access_token, verify_password


class AuthService:
    def __init__(self, session: AsyncSession):
        self.dao = SuperAdminDAO(session)

    async def authenticate_super_admin(self, login_data: SuperAdminLogin) -> Token:
        """Authenticate super admin and return token."""
        admin = await self.dao.get_by_email(login_data.email)

        if not admin or not verify_password(login_data.password, admin.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token with super admin flag
        access_token = create_access_token(data={"sub": admin.email, "is_super_admin": True})

        return Token(access_token=access_token)
