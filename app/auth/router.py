from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import SuperAdminLogin, Token
from app.auth.services import AuthService
from app.database.session import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


@router.post("/login", response_model=Token)
async def login(login_data: SuperAdminLogin, service: AuthService = Depends(get_auth_service)):
    """Login endpoint for super admin."""
    return await service.authenticate_super_admin(login_data)
