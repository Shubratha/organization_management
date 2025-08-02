from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.database.dao import BaseDAO
from app.database.session import create_database
from app.organization.models import Organization
from app.organization.schemas import OrgCreate, OrgRetrieve


class OrganizationDAO(BaseDAO[Organization, OrgCreate, OrgRetrieve]):
    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)

    async def create_organization(self, org_data: OrgCreate) -> Organization:
        """Create a new organization with its own database."""
        # Create new database and user for the organization
        db_user = f"user_{org_data.organization_name.lower()}"
        db_pass = f"org_pass_{org_data.password}"
        db_name = org_data.organization_name.lower()

        db_url = await create_database(db_name, db_user, db_pass)

        # Create organization record
        org = Organization(
            name=org_data.organization_name,
            db_url=db_url,
            admin_email=org_data.email,
            admin_password=get_password_hash(org_data.password),
        )
        self.session.add(org)
        await self.session.commit()
        await self.session.refresh(org)
        return org

    async def get_by_name(self, name: str) -> Optional[Organization]:
        """Get organization by name."""
        result = await self.session.execute(select(Organization).where(Organization.name.ilike(name)))
        return result.scalars().first()

    async def get_by_admin_email(self, email: str) -> Optional[Organization]:
        """Get organization by admin email."""
        result = await self.session.execute(select(Organization).where(Organization.admin_email == email))
        return result.scalars().first()

    async def exists_by_name(self, name: str) -> bool:
        """Check if organization exists by name."""
        org = await self.get_by_name(name)
        return org is not None
