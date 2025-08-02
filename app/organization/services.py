from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.organization.dao import OrganizationDAO
from app.organization.models import Organization
from app.organization.schemas import AdminLogin, OrgCreate, Token


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.dao = OrganizationDAO(session)

    async def create_organization(self, org_data: OrgCreate) -> Organization:
        """Create a new organization with its database."""
        # Check if organization exists
        if await self.dao.exists_by_name(org_data.organization_name):
            raise HTTPException(status_code=400, detail="Organization already exists")

        try:
            org = await self.dao.create_organization(org_data)
            return org
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create organization: {str(e)}")

    async def get_organization(self, name: str) -> Organization:
        """Get organization by name."""
        org = await self.dao.get_by_name(name)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return org

    async def admin_login(self, login_data: AdminLogin) -> Token:
        """Handle admin login and token generation."""
        org = await self.dao.get_by_admin_email(login_data.email)

        if not org or not verify_password(login_data.password, org.admin_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": login_data.email, "org": org.name})

        return Token(access_token=access_token)
